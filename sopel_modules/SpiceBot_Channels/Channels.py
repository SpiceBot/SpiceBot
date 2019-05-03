#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.tools import stderr
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute

import time

import spicemanip

from sopel_modules.SpiceBot_SBTools import (
                                            sopel_triggerargs, inlist, topic_compile, channel_privs,
                                            join_all_channels, chanadmin_all_channels, channel_list_current
                                            )


class SpiceBot_Channels_MainSection(StaticSection):
    announcenew = ValidatedAttribute('announcenew', default=False)
    joinall = ValidatedAttribute('joinall', default=False)
    operadmin = ValidatedAttribute('operadmin', default=False)
    chanignore = ListAttribute('chanignore')


def configure(config):
    config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
    config.SpiceBot_Channels.configure_setting('announcenew', 'SpiceBot_Channels Announce New Channels')
    config.SpiceBot_Channels.configure_setting('announcenew', 'SpiceBot_Channels JOIN New Channels')
    config.SpiceBot_Channels.configure_setting('announcenew', 'SpiceBot_Channels OPER ADMIN MODE')
    config.SpiceBot_Channels.configure_setting('chanignore', 'SpiceBot_Channels Ignore JOIN for channels')


def setup(bot):
    stderr("[SpiceBot_Channels] Initial Setup processing...")

    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)

    bot.memory['SpiceBot_Channels'] = dict()
    bot.memory['SpiceBot_Channels']['channels'] = dict()
    bot.memory['SpiceBot_Channels']['InitialProcess'] = False
    bot.memory['SpiceBot_Channels']['ProcessLock'] = False


@sopel.module.event('001')
@sopel.module.rule('.*')
def trigger_channel_list_initial(bot, trigger):

    # Unkickable
    bot.write(('SAMODE', bot.nick, '+q'))

    bot.write(['LIST'])
    bot.memory['SpiceBot_Channels']['ProcessLock'] = True

    stderr("[SpiceBot_Channels] Initial Channel list populating...")
    starttime = time.time()

    while not bot.memory['SpiceBot_Channels']['InitialProcess']:
        timesince = time.time() - starttime
        if timesince < 60:
            pass
        else:
            stderr("[SpiceBot_Channels] Initial Channel list populating Timed Out.")
            bot.memory['SpiceBot_Channels']['InitialProcess'] = True

    channel_list_current(bot)
    foundchannelcount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
    stderr("[SpiceBot_Channels] Channel listing finished! " + str(foundchannelcount) + " channel(s) found.")

    join_all_channels(bot)
    chanadmin_all_channels(bot)

    if "*" in bot.memory['SpiceBot_Channels']['channels']:
        del bot.memory['SpiceBot_Channels']['channels']["*"]

    while True:
        time.sleep(1800)
        oldlist = list(bot.memory['SpiceBot_Channels']['channels'].keys())
        bot.write(['LIST'])
        bot.memory['SpiceBot_Channels']['ProcessLock'] = True

        while bot.memory['SpiceBot_Channels']['ProcessLock']:
            pass

        newlist = [item.lower() for item in oldlist if item.lower() not in bot.memory['SpiceBot_Channels']['channels']]
        if "*" in newlist:
            newlist.remove("*")
        if len(newlist) and bot.config.SpiceBot_Channels.announcenew:
            bot.osd(["The Following channel(s) are new:", spicemanip.main(newlist, 'andlist')], bot.channels.keys())

        join_all_channels(bot)

        chanadmin_all_channels(bot)

        if "*" in bot.memory['SpiceBot_Channels']['channels']:
            del bot.memory['SpiceBot_Channels']['channels']["*"]


@sopel.module.event('321')
@sopel.module.rule('.*')
def watch_chanlist_start(bot, trigger):
    bot.memory['SpiceBot_Channels']['ProcessLock'] = True


@sopel.module.event('322')
@sopel.module.rule('.*')
def watch_chanlist_populate(bot, trigger):
    channel, _, topic = trigger.args[1:]
    if channel.lower() not in bot.memory['SpiceBot_Channels']['channels']:
        bot.memory['SpiceBot_Channels']['channels'][channel.lower()] = dict()
        bot.memory['SpiceBot_Channels']['channels'][channel.lower()]['name'] = channel
        bot.memory['SpiceBot_Channels']['channels'][channel.lower()]['topic'] = topic_compile(topic)
    bot.memory['SpiceBot_Channels']['ProcessLock'] = True


@sopel.module.event('323')
@sopel.module.rule('.*')
def watch_chanlist_complete(bot, trigger):
    bot.memory['SpiceBot_Channels']['ProcessLock'] = False
    if not bot.memory['SpiceBot_Channels']['InitialProcess']:
        bot.memory['SpiceBot_Channels']['InitialProcess'] = True


@sopel.module.nickname_commands('channels', 'channel')
def nickname_comand_chanstats(bot, trigger):

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    if not len(triggerargs):
        commandused = 'list'
    else:
        commandused = spicemanip.main(triggerargs, 1).lower()

    triggerargs = spicemanip.main(triggerargs, '2+', 'list')

    channel_list_current(bot)

    if commandused == 'list':
        chanlist = spicemanip.main(bot.channels.keys(), 'andlist')
        bot.osd("You can find me in " + chanlist)
        return

    elif commandused == 'total':
        botcount = len(bot.channels.keys())
        servercount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
        bot.osd("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")
        return

    elif commandused == 'random':
        channel = spicemanip.main(bot.memory['SpiceBot_Channels']['channels'], 'random')
        topic = bot.memory['SpiceBot_Channels']['channels'][channel]['topic']
        msg = ["Random channel for you: {}.".format(bot.memory['SpiceBot_Channels']['channels'][channel]['name'])]
        if topic and not topic.isspace():
            msg.append("The topic is: {}".format(topic))
        else:
            msg.append("Its topic is empty.")
        bot.osd(msg)
        return

    elif commandused == 'update':
        if not trigger.admin:
            bot.osd("You do not have permission to update the channel listing.")
            return
        bot.write(['LIST'])
        bot.osd(["[SpiceBot_Channels]", "I am now updating the channel listing for this server."])
        bot.memory['SpiceBot_Channels']['ProcessLock'] = True
        while bot.memory['SpiceBot_Channels']['ProcessLock']:
            pass
        foundchannelcount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
        bot.osd("[SpiceBot_Channels]", "Channel listing finished!", str(foundchannelcount) + " channel(s) found.")
        return

    elif commandused == 'topic':
        if not len(triggerargs):
            bot.osd("Channel name input missing.")
            return
        channel = spicemanip.main(triggerargs, 1)
        if not inlist(bot, channel.lower(), bot.memory['SpiceBot_Channels']['channels'].keys()):
            bot.osd("Channel name {} not valid.".format(channel))
            return
        topic = bot.memory['SpiceBot_Channels']['channels'][channel.lower()]['topic']
        channel = bot.memory['SpiceBot_Channels']['channels'][channel.lower()]['name']
        bot.osd("Topic for {}: {}".format(channel, topic))
        return

    if commandused.upper() in ['OP', 'HOP', 'VOICE', 'OWNER', 'ADMIN']:
        if not len(triggerargs):
            if trigger.is_privmsg:
                bot.osd("Channel name required.")
                return
            else:
                channel = trigger.sender
        else:
            channel = spicemanip.main(triggerargs, 1)
            if not inlist(bot, channel.lower(), bot.memory['SpiceBot_Channels']['channels'].keys()):
                bot.osd("Channel name {} not valid.".format(channel))
                return
            if not inlist(bot, channel.lower(), bot.channels.keys()):
                bot.osd("I need to be in {} to see nick privileges.".format(channel))
                return

        privlist = channel_privs(bot, channel, commandused.upper())
        dispmsg = []
        if not len(privlist):
            dispmsg.append("There are no Channel " + commandused.upper() + "s for " + str(channel))
        else:
            oplist = spicemanip.main(privlist, 'andlist')
            dispmsg.append("Channel " + commandused.upper() + "s for " + str(channel) + "  are: " + oplist)
        bot.osd(dispmsg, trigger.nick, 'notice')
        return

    # Users List
    if commandused == 'users':
        channel = spicemanip.main(triggerargs, 1)
        if not inlist(bot, channel.lower(), bot.memory['SpiceBot_Channels']['channels'].keys()):
            bot.osd("Channel name {} not valid.".format(channel))
            return
        if not inlist(bot, channel.lower(), bot.channels.keys()):
            bot.osd("I need to be in {} to see user list.".format(channel))
            return
        dispmsg = []
        if not len(bot.channels[channel].privileges.keys()):
            dispmsg.append("There are no Channel users for " + str(channel))
        else:
            userslist = spicemanip.main(bot.channels[channel].privileges.keys(), 'andlist')
            dispmsg.append("Channel users for " + str(channel) + " are: " + userslist)
        bot.osd(dispmsg, trigger.nick, 'notice')
        return
