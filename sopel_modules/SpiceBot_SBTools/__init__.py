# coding=utf-8
"""Useful miscellaneous tools and shortcuts for SpiceBot Sopel modules
"""
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.module import OP, ADMIN, VOICE, OWNER, HALFOP
from sopel.tools import stderr
HOP = HALFOP

import collections
import re
import os

import spicemanip


"""Sopel Wrapping Tools"""


def sopel_triggerargs(bot, trigger, command_type):
    triggerargs = []

    if len(trigger.args) > 1:
        triggerargs = spicemanip.main(trigger.args[1], 'create')
    triggerargs = spicemanip.main(triggerargs, 'create')

    if command_type in ['module_command']:
        triggerargs = spicemanip.main(triggerargs, '2+', 'list')
    elif command_type in ['nickname_command']:
        triggerargs = spicemanip.main(triggerargs, '3+', 'list')

    return triggerargs


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


"""Channel Functions"""


def topic_compile(topic):
    actual_topic = re.compile(r'^\[\+[a-zA-Z]+\] (.*)')
    topic = re.sub(actual_topic, r'\1', topic)
    return topic


def channel_privs(bot, channel):

    if channel not in bot.memory['SpiceBot_Channels']['channels'].keys():
        topic = bot.channels[channel].topic
        bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()] = dict()
        bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()]['name'] = str(channel)
        bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()]['topic'] = topic_compile(topic)

    for chan in bot.memory['SpiceBot_Channels']['channels'].keys():
        for privtype in ['VOICE', 'HOP', 'OP', 'ADMIN', 'OWNER']:
            if privtype not in bot.memory['SpiceBot_Channels']['channels'][str(chan).lower()].keys():
                bot.memory['SpiceBot_Channels']['channels'][str(chan).lower()][privtype] = []

    for user in bot.channels[channel].privileges.keys():
        try:
            privnum = bot.channels[channel].privileges[user] or 0
        except KeyError:
            privnum = 0

        for privtype in ['VOICE', 'HOP', 'OP', 'ADMIN', 'OWNER']:
            if privnum == eval(privtype) or (privnum >= eval(privtype) and privtype == 'OWNER'):
                if user not in bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()][privtype]:
                    bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()][privtype].append(user)
            else:
                if user in bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()][privtype]:
                    bot.memory['SpiceBot_Channels']['channels'][str(channel).lower()][privtype].remove(user)


def join_all_channels(bot):
    if bot.config.SpiceBot_Channels.joinall:
        for channel in bot.memory['SpiceBot_Channels']['channels'].keys():
            if channel not in bot.channels.keys() and channel not in bot.config.SpiceBot_Channels.chanignore:
                bot.write(('JOIN', bot.nick, bot.memory['SpiceBot_Channels']['channels'][channel]['name']))
                if channel not in bot.channels.keys():
                    bot.write(('SAJOIN', bot.nick, bot.memory['SpiceBot_Channels']['channels'][channel]['name']))


def chanadmin_all_channels(bot):
    # Chan ADMIN +a
    for channel in bot.channels.keys():
        if channel not in bot.config.SpiceBot_Channels.chanignore:
            if bot.config.SpiceBot_Channels.operadmin:
                if not bot.channels[channel].privileges[bot.nick] < ADMIN:
                    bot.write(('SAMODE', channel, "+a", bot.nick))
            channel_privs(bot, channel)
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


def service_manip(bot, servicename, dowhat):
    if str(dowhat) not in ["start", "stop", "restart"]:
        return
    try:
        stderr(str(dowhat).title() + "ing " + str(servicename) + ".service.")
        os.system("sudo service " + str(servicename) + " " + str(dowhat))
    except Exception as e:
        stderr(str(dowhat).title() + "ing " + str(servicename) + ".service Failed: " + str(e))


def spicebot_update(bot):
    try:
        stderr("Updating " + bot.nick + " from Github.")
        for line in os.popen("pip3 install --upgrade --no-deps --force-reinstall git+" +
                    str(bot.config.SpiceBot_Update.gitrepo) +
                    "@" + str(bot.config.SpiceBot_Update.gitbranch)).read().split('\n'):
            stderr(line)
    except Exception as e:
        stderr("Updating " + bot.nick + " from Github Failed:" + str(e))
