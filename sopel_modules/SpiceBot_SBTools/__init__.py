#!/usr/bin/env python
# coding=utf-8
"""Useful miscellaneous tools and shortcuts for SpiceBot Sopel modules
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import sopel

import collections
import re
import os
import sys
import codecs
import requests
from fake_useragent import UserAgent
from difflib import SequenceMatcher
from operator import itemgetter
from collections import abc
from pygit2 import clone_repository

import spicemanip


"""Variable References"""

github_dict = {
                "url_main": "https://github.com/",
                "url_api": "https://api.github.com/repos/",
                "url_raw": "https://raw.githubusercontent.com/",
                "url_path_wiki": "/wiki",
                "url_path_issues": "/issues",
                "repo_owner": "SpiceBot",
                "repo_name": "SpiceBot",
                }


"""Sopel Wrapping Tools"""


def sopel_triggerargs(bot, trigger, command_type='module_command'):
    triggerargs = []

    if len(trigger.args) > 1:
        triggerargs = spicemanip.main(trigger.args[1], 'create')
    triggerargs = spicemanip.main(triggerargs, 'create')

    if command_type in ['nickname_command']:
        command = spicemanip.main(triggerargs, 2).lower()
        triggerargs = spicemanip.main(triggerargs, '3+', 'list')
    else:
        command = spicemanip.main(triggerargs, 1).lower()[1:]
        triggerargs = spicemanip.main(triggerargs, '2+', 'list')

    return triggerargs, command


def bot_privs(bot, privtype):
    if privtype == 'owners':
        privtype = 'owner'
    botpriveval = eval("bot.config.core." + privtype)
    if not isinstance(botpriveval, list):
        botpriveval = [botpriveval]
    return botpriveval


def command_permissions_check(bot, trigger, privslist):

    commandrunconsensus = []

    for botpriv in ["admins", "owner"]:
        if botpriv in privslist:
            botpriveval = bot_privs(bot, botpriv)
            if not inlist(bot, trigger.nick, botpriveval):
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')

    if not trigger.is_privmsg:
        for chanpriv in ['OP', 'HOP', 'VOICE', 'OWNER', 'ADMIN']:
            if chanpriv in privslist:
                chanpriveval = channel_privs(bot, trigger.sender, chanpriv)
                if not inlist(bot, trigger.nick, chanpriveval):
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')

    if not len(privslist):
        commandrunconsensus.append('True')

    if 'True' not in commandrunconsensus:
        return False

    return True


"""Logging"""


def bot_logging(bot, logtype, logentry, stdio=False):

    if 'SpiceBot_Logs' not in bot.memory:
        bot.memory['SpiceBot_Logs'] = {"logs": {"Sopel_systemd": [], "Sopel_stdio": []}, "queue": []}

    logmessage = "[" + logtype + "] " + logentry + ""

    bot.memory['SpiceBot_Logs']["queue"].append(logmessage)

    if stdio:
        sopel.tools.stderr(logmessage)

    if logtype not in bot.memory['SpiceBot_Logs']["logs"].keys():
        bot.memory['SpiceBot_Logs']["logs"][logtype] = []

    bot.memory['SpiceBot_Logs']["logs"][logtype].append(logentry)
    if len(bot.memory['SpiceBot_Logs']["logs"][logtype]) > 10:
        del bot.memory['SpiceBot_Logs']["logs"][logtype][0]


"""
Time
"""


def humanized_time(countdownseconds):
    time = float(countdownseconds)
    if time == 0:
        return "just now"
    year = time // (365 * 24 * 3600)
    time = time % (365 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = None
    timearray = ['year', 'day', 'hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            if displaymsg:
                displaymsg = str(displaymsg + " " + str(int(currenttimevar)) + " " + timetype)
            else:
                displaymsg = str(str(int(currenttimevar)) + " " + timetype)
    if not displaymsg:
        return "just now"
    return displaymsg
    eval(year + day + hour + minute + second)


"""Online Information Requests"""


def googlesearch(bot, searchterm, searchtype=None):
    header = {'User-Agent': str(UserAgent().chrome)}
    data = searchterm.replace(' ', '+')
    lookfor = data.replace(':', '%3A')
    try:
        if searchtype == 'maps':
            var = requests.get(r'http://www.google.com/maps/place/' + lookfor, headers=header)
        else:
            var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI', headers=header)
    except Exception as e:
        var = e
        var = None

    if not var or not var.url:
        return None
    else:
        return var.url


"""List Manipulation Functions"""


def inlist(bot, searchterm, searchlist):

    # verify we are searching a list
    if isinstance(searchlist, collections.abc.KeysView) or isinstance(searchlist, dict):
        searchlist = [x for x in searchlist]
    if not isinstance(searchlist, list):
        searchlist = [searchlist]
    rebuildlist = []
    for searchitem in searchlist:
        rebuildlist.append(str(searchitem))

    searchterm = str(searchterm)

    if searchterm in rebuildlist:
        return True
    elif searchterm.lower() in [searching.lower() for searching in rebuildlist]:
        return True
    else:
        return False


def inlist_match(bot, searchterm, searchlist):
    # verify we are searching a list
    if isinstance(searchlist, collections.abc.KeysView) or isinstance(searchlist, dict):
        searchlist = [x for x in searchlist]
    if not isinstance(searchlist, list):
        searchlist = [searchlist]
    rebuildlist = []
    for searchitem in searchlist:
        rebuildlist.append(str(searchitem))

    searchterm = str(searchterm)
    if searchterm in rebuildlist:
        return searchterm
    else:
        for searching in rebuildlist:
            if searching.lower() == searchterm.lower():
                return searching
    return searchterm


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def similar_list(bot, searchitem, searchlist, matchcount=1, searchorder='reverse'):

    if sys.version_info.major >= 3:
        if isinstance(searchlist, abc.KeysView):
            searchlist = [x for x in searchlist]
    if isinstance(searchlist, dict):
        searchlist = [x for x in searchlist]

    if not isinstance(searchlist, list):
        searchlist = [searchlist]

    sim_listitems, sim_num = [], []
    for listitem in searchlist:
        similarlevel = SequenceMatcher(None, searchitem.lower(), listitem.lower()).ratio()
        if similarlevel >= .75:
            sim_listitems.append(listitem)
            sim_num.append(similarlevel)

    if len(sim_listitems) and len(sim_num):
        sim_num, sim_listitems = (list(x) for x in zip(*sorted(zip(sim_num, sim_listitems), key=itemgetter(0))))

    if searchorder == 'reverse':
        sim_listitems = spicemanip.main(sim_listitems, 'reverse', "list")

    sim_listitems[-matchcount:]

    return sim_listitems


def array_arrangesort(bot, sortbyarray, arrayb):
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb), key=itemgetter(0))))
    return sortbyarray, arrayb


def letters_in_string(text):
    if text.isupper() or text.islower():
        return True
    else:
        return False


"""Channel Functions"""


def topic_compile(topic):
    actual_topic = re.compile(r'^\[\+[a-zA-Z]+\] (.*)')
    topic = re.sub(actual_topic, r'\1', topic)
    return topic


def channel_privs(bot, channel, privtype):
    privlist = []
    for user in bot.channels[channel].privileges.keys():
        try:
            privnum = bot.channels[channel].privileges[user] or 0
        except KeyError:
            privnum = 0
        if privtype == 'HOP':
            privtypeeval = sopel.module.HALFOP
        else:
            privtypeeval = eval("sopel.module." + privtype)
        if (privnum == privtypeeval or
                (privnum >= privtypeeval and privtype == 'OWNER') or
                (privnum >= privtypeeval and privnum < sopel.module.OWNER and privtype == 'ADMIN')):
            privlist.append(user)
    return privlist


def join_all_channels(bot):
    if bot.config.SpiceBot_Channels.joinall:
        for channel in bot.memory['SpiceBot_Channels']['channels'].keys():
            if channel not in bot.channels.keys() and channel not in bot.config.SpiceBot_Channels.chanignore:
                bot.write(('JOIN', bot.nick, bot.memory['SpiceBot_Channels']['channels'][channel]['name']))
                if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                    bot.write(('SAJOIN', bot.nick, bot.memory['SpiceBot_Channels']['channels'][channel]['name']))


def chanadmin_all_channels(bot):
    # Chan ADMIN +a
    for channel in bot.channels.keys():
        if channel not in bot.config.SpiceBot_Channels.chanignore:
            if bot.config.SpiceBot_Channels.operadmin:
                if not bot.channels[channel].privileges[bot.nick] < sopel.module.ADMIN:
                    bot.write(('SAMODE', channel, "+a", bot.nick))
        else:
            bot.part(channel)


def channel_list_current(bot):
    newlist = [item for item in bot.channels.keys() if item.lower() not in bot.memory['SpiceBot_Channels']['channels']]
    for channel in newlist:
        topic = bot.channels[channel].topic
        bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()] = dict()
        bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()]['name'] = str(channel)
        bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()]['topic'] = topic_compile(topic)

    if "*" in bot.memory['SpiceBot_Channels']:
        bot.memory['SpiceBot_Channels'].remove("*")


"""Environment Functions"""


def stock_modules_begone(bot):

    # Remove stock modules, if present
    main_sopel_dir = os.path.dirname(os.path.abspath(sopel.__file__))
    modules_dir = os.path.join(main_sopel_dir, 'modules')
    stockdir = os.path.join(modules_dir, "stock")
    if not os.path.exists(stockdir) or not os.path.isdir(stockdir):
        os.system("sudo mkdir " + stockdir)
    if "SpiceBot_dummycommand.py" not in os.listdir(modules_dir):
        import sopel_modules
        for plugin_dir in set(sopel_modules.__path__):
            for pathname in os.listdir(plugin_dir):
                if pathname == 'SpiceBot_SopelPatches':
                    pypi_modules_dir = os.path.join(plugin_dir, pathname)
                    if "SpiceBot_dummycommand.py" in os.listdir(pypi_modules_dir):
                        if "SpiceBot_dummycommand.py" not in os.listdir(modules_dir):
                            os.system("sudo cp " + os.path.join(pypi_modules_dir, "SpiceBot_dummycommand.py") + " " + os.path.join(modules_dir, "SpiceBot_dummycommand.py"))
    for pathname in os.listdir(modules_dir):
        path = os.path.join(modules_dir, pathname)
        if (os.path.isfile(path) and pathname.endswith('.py') and not pathname.startswith('_')):
            if not pathname in ["__init__.py", "SpiceBot_dummycommand.py"]:
                os.system("sudo mv " + path + " " + stockdir)


def spicebot_update(bot, deps=False):

    if not os.path.exists("/tmp") or not os.path.isdir("/tmp"):
        os.system("sudo mkdir /tmp")
    clonepath = "/tmp/SpiceBot"
    if not os.path.exists(clonepath) or not os.path.isdir(clonepath):
        os.system(clonepath)

    bot_logging(bot, 'SpiceBot_Update', "Cloning  to " + clonepath, True)

    clone_repository(str(bot.config.SpiceBot_Update.gitrepo + ".git"), clonepath, checkout_branch=bot.config.SpiceBot_Update.gitbranch)

    pipcommand = "sudo pip3 install --upgrade"
    if not deps:
         pipcommand += " --no-deps"
    pipcommand += " --force-reinstall"
    # pipcommand += " git+" + str(bot.config.SpiceBot_Update.gitrepo) + "@" + str(bot.config.SpiceBot_Update.gitbranch)
    pipcommand += " /tmp/SpiceBot/"

    bot_logging(bot, 'SpiceBot_Update', "Running `" + pipcommand + "`", True)
    # for line in os.popen(pipcommand).read().split('\n'):
    #    bot_logging(bot, 'SpiceBot_Update', "    " + line)
    os.system(pipcommand)

    bot_logging(bot, 'SpiceBot_Update', "Deleting " + clonepath, True)

    os.system("sudo rm -r /tmp/SpiceBot")

    stock_modules_begone(bot)


def spicebot_reload(bot, log_from='service_manip', quitmessage='Recieved QUIT'):
    # service_manip(bot, bot.nick, 'restart', log_from)
    bot.restart(quitmessage)


def service_manip(bot, servicename, dowhat, log_from='service_manip'):
    if str(dowhat) not in ["start", "stop", "restart"]:
        return
    try:
        bot_logging(bot, log_from, str(dowhat).title() + "ing " + str(servicename) + ".service.")
        os.system("sudo service " + str(servicename) + " " + str(dowhat))
    except Exception as e:
        bot_logging(bot, log_from, str(dowhat).title() + "ing " + str(servicename) + ".service Failed: " + str(e))


"""Config Reading Functions"""


def read_directory_json_to_dict(bot, directories, configtypename="Config File", log_from='read_directory_json_to_dict'):

    if not isinstance(directories, list):
        directories = [directories]

    configs_dict = {}
    filesprocess, fileopenfail, filecount = [], 0, 0
    for directory in directories:
        if os.path.exists(directory) and os.path.isdir(directory):
            if len(os.listdir(directory)) > 0:
                for file in os.listdir(directory):
                    filepath = os.path.join(directory, file)
                    if os.path.isfile(filepath):
                        filesprocess.append(filepath)

    for filepath in filesprocess:

        # Read dictionary from file, if not, enable an empty dict
        filereadgood = True
        inf = codecs.open(filepath, "r", encoding='utf-8')
        infread = inf.read()
        try:
            dict_from_file = eval(infread)
        except Exception as e:
            filereadgood = False
            if bot:
                bot_logging(bot, log_from, "Error loading %s: %s (%s)" % (configtypename, e, filepath))
            dict_from_file = dict()
        # Close File
        inf.close()

        if filereadgood and isinstance(dict_from_file, dict):
            filecount += 1
            slashsplit = str(filepath).split("/")
            filename = slashsplit[-1]
            configs_dict[filename] = dict_from_file
        else:
            fileopenfail += 1

    if filecount:
        if bot:
            bot_logging(bot, log_from, 'Registered %d %s dict files,' % (filecount, configtypename))
            bot_logging(bot, log_from, '%d %s dict files failed to load' % (fileopenfail, configtypename), True)
    else:
        if bot:
            bot_logging(bot, log_from, "Warning: Couldn't load any %s dict files" % (configtypename))

    return configs_dict
