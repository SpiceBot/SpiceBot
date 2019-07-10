#!/usr/bin/env python
# coding=utf-8
"""Useful miscellaneous tools and shortcuts for SpiceBot Sopel modules
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import sopel

import collections
import os
import sys
from difflib import SequenceMatcher
from operator import itemgetter
from collections import abc
from pygit2 import clone_repository

from sopel_modules.spicemanip import spicemanip

from .Logs import logs
from .Config import config as botconfig


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

mode_dict_alias = {
                    "+o": "OP", "-o": "deOP",
                    "+v": "VOICE", "-v": "deVOICE",
                    "+h": "HOP", "-h": "deHOP",
                    "+a": "ADMIN", "-a": "deADMIN",
                    "+q": "OWNER", "-q": "deOWNER",
                    "+b": "BAN", "-b": "unBAN",
                    "+c": "noCOLOR", "-c": "COLOR",
                    #  TODO add more user/channel modes
                    }


"""Sopel Wrapping Tools"""


def bot_privs(privtype):
    if privtype == 'owners':
        privtype = 'owner'
    botpriveval = eval("botconfig." + privtype)
    if not isinstance(botpriveval, list):
        botpriveval = [botpriveval]
    return botpriveval


def command_permissions_check(bot, trigger, privslist):

    commandrunconsensus = []

    for botpriv in ["admins", "owner"]:
        if botpriv in privslist:
            botpriveval = bot_privs(botpriv)
            if not inlist(trigger.nick, botpriveval):
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')

    if not trigger.is_privmsg:
        for chanpriv in ['OP', 'HOP', 'VOICE', 'OWNER', 'ADMIN']:
            if chanpriv in privslist:
                chanpriveval = channel_privs(bot, trigger.sender, chanpriv)
                if not inlist(trigger.nick, chanpriveval):
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')

    if not len(privslist):
        commandrunconsensus.append('True')

    if 'True' not in commandrunconsensus:
        return False

    return True


"""
Classes
"""


def class_create(classname):
    compiletext = """
        def __init__(self):
            self.default = str(self.__class__.__name__)
        def __repr__(self):
            return repr(self.default)
        def __str__(self):
            return str(self.default)
        def __iter__(self):
            return str(self.default)
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext, "", "exec"))
    newclass = eval('class_'+classname+"()")
    return newclass


def class_directory(inputclass):

    # make sure input is a class
    # if not isinstance(inputclass, class):
        # return []

    classdirlistfull, classdirlistclean = dir(inputclass), []
    for classdiritem in classdirlistfull:
        if not classdiritem.startswith("_"):
            classdirlistclean.append(classdiritem)
    return classdirlistclean


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


"""List Manipulation Functions"""


def inlist(searchterm, searchlist):

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


def inlist_match(searchterm, searchlist):
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


def similar_list(searchitem, searchlist, matchcount=1, searchorder='reverse'):

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
        sim_listitems = spicemanip(sim_listitems, 'reverse', "list")

    sim_listitems[-matchcount:]

    return sim_listitems


def array_arrangesort(sortbyarray, arrayb):
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb), key=itemgetter(0))))
    return sortbyarray, arrayb


def letters_in_string(text):
    if text.isupper() or text.islower():
        return True
    else:
        return False


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


"""Channel Functions"""


def channel_privs(bot, channel, privtype):
    privlist = []
    for user in list(bot.channels[channel].privileges.keys()):
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


"""Environment Functions"""


def stock_modules_begone():

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


def spicebot_update(deps=False):

    if not os.path.exists("/tmp") or not os.path.isdir("/tmp"):
        os.system("sudo mkdir /tmp")
    clonepath = "/tmp/SpiceBot"
    if not os.path.exists(clonepath) or not os.path.isdir(clonepath):
        os.system(clonepath)

    logs.log('SpiceBot_Update', "Cloning  to " + clonepath, True)

    clone_repository(str(botconfig.SpiceBot_Update.gitrepo + ".git"), clonepath, checkout_branch=botconfig.SpiceBot_Update.gitbranch)

    pipcommand = "sudo pip3 install --upgrade"
    if not deps:
         pipcommand += " --no-deps"
    pipcommand += " --force-reinstall"
    # pipcommand += " git+" + str(botconfig.SpiceBot_Update.gitrepo) + "@" + str(botconfig.SpiceBot_Update.gitbranch)
    pipcommand += " /tmp/SpiceBot/"

    logs.log('SpiceBot_Update', "Running `" + pipcommand + "`", True)
    # for line in os.popen(pipcommand).read().split('\n'):
    #    logs.log('SpiceBot_Update', "    " + line)
    os.system(pipcommand)

    logs.log('SpiceBot_Update', "Deleting " + clonepath, True)

    os.system("sudo rm -r /tmp/SpiceBot")

    stock_modules_begone()


def spicebot_reload(bot, log_from='service_manip', quitmessage='Recieved QUIT'):
    # service_manip(bot.nick, 'restart', log_from)
    bot.restart(quitmessage)


def service_manip(servicename, dowhat, log_from='service_manip'):
    if str(dowhat) not in ["start", "stop", "restart"]:
        return
    try:
        logs.log(log_from, str(dowhat).title() + "ing " + str(servicename) + ".service.")
        os.system("sudo service " + str(servicename) + " " + str(dowhat))
    except Exception as e:
        logs.log(log_from, str(dowhat).title() + "ing " + str(servicename) + ".service Failed: " + str(e))
