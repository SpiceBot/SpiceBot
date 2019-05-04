# coding=utf-8
"""Useful miscellaneous tools and shortcuts for SpiceBot Sopel modules
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import sopel
from sopel.module import OP, ADMIN, VOICE, OWNER, HALFOP
from sopel.tools import stderr
HOP = HALFOP

import collections
import re
import os
import codecs

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

    if privslist == []:
        commandrunconsensus.append('True')

    if 'True' not in commandrunconsensus:
        return False

    return True


"""Logging"""


def bot_logging(bot, logtype, logentry):

    if 'SpiceBot_Logs_queue' not in bot.memory:
        bot.memory['SpiceBot_Logs_queue'] = []

    logmessage = "[" + logtype + "] " + logentry + ""

    if bot.config.SpiceBot_Logs.logging_channel:
        bot.memory['SpiceBot_Logs_queue'].append(logmessage)

    stderr("\n" + logmessage + "\n")

    if 'SpiceBot_Logs' not in bot.memory:
        bot.memory['SpiceBot_Logs'] = {}

    if logtype not in bot.memory['SpiceBot_Logs'].keys():
        bot.memory['SpiceBot_Logs'][logtype] = []

    bot.memory['SpiceBot_Logs'][logtype].append(logentry)
    if len(bot.memory['SpiceBot_Logs'][logtype]) > 10:
        del bot.memory['SpiceBot_Logs'][logtype][0]


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
        if (privnum == eval(privtype) or
                (privnum >= eval(privtype) and privtype == 'OWNER') or
                (privnum >= eval(privtype) and privnum < eval("OWNER") and privtype == 'ADMIN')):
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
                if not bot.channels[channel].privileges[bot.nick] < ADMIN:
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
        channel_privs(bot, channel)

    if "*" in bot.memory['SpiceBot_Channels']:
        bot.memory['SpiceBot_Channels'].remove("*")


"""Environment Functions"""


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
            bot_logging(bot, log_from, 'Registered %d %s files,' % (filecount, configtypename))
            bot_logging(bot, log_from, '%d %s files failed to load' % (fileopenfail, configtypename))
    else:
        if bot:
            bot_logging(bot, log_from, "Warning: Couldn't load any %s files" % (configtypename))

    return configs_dict
