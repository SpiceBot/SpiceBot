# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

from sopel_modules.SpiceBot_Events.System import botevents
from sopel_modules.SpiceBot_SBTools import (
                                            sopel_triggerargs, inlist, channel_privs,
                                            join_all_channels, channel_list_current,
                                            )
from .Channels import bot_part_empty


@botevents.check_ready([botevents.BOT_LOADED])
@sopel.module.nickname_commands('channels', 'channel')
def nickname_comand_channels(bot, trigger):

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
        bot_part_empty(bot)
        bot.write(['LIST'])
        bot.osd(["[SpiceBot_Channels]", "I am now updating the channel listing for this server."])
        bot.memory['SpiceBot_Channels']['ProcessLock'] = True
        while bot.memory['SpiceBot_Channels']['ProcessLock']:
            pass
        join_all_channels(bot)
        foundchannelcount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
        bot.osd("[SpiceBot_Channels]", "Channel listing finished!", str(foundchannelcount) + " channel(s) found.")
        bot_part_empty(bot)
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
