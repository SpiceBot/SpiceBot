# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel

from sopel_modules.spicemanip import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('channels', 'channel')
def nickname_comand_channels(bot, trigger, botcom):

    if not len(botcom.dict['args']):
        commandused = 'list'
    else:
        commandused = spicemanip(botcom.dict['args'], 1).lower()

    botcom.dict['args'] = spicemanip(botcom.dict['args'], '2+', 'list')

    if commandused == 'list':
        botcount = SpiceBot.channels.total_bot_channels()
        servercount = SpiceBot.channels.total_channels()
        displayval = "I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server."
        chanlist = spicemanip(SpiceBot.channels.chanlist_bot(), 'andlist')
        bot.osd([displayval, "You can find me in " + chanlist])
        return

    elif commandused == 'total':
        botcount = SpiceBot.channels.total_bot_channels()
        servercount = SpiceBot.channels.total_channels()
        bot.osd("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")
        return

    elif commandused == 'random':
        channel = spicemanip(list(SpiceBot.channels.chandict), 'random')
        topic = SpiceBot.channels.chandict[channel]['topic']
        msg = ["Random channel for you: {}.".format(SpiceBot.channels.chandict[channel]['name'])]
        if topic and not topic.isspace():
            msg.append("The topic is: {}".format(topic))
        else:
            msg.append("Its topic is empty.")
        bot.osd(msg)
        return

    elif commandused == 'update':
        if not trigger.admin:  # TODO
            SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "You do not have permission to update the channel listing.")
            return
        SpiceBot.channels.bot_part_empty(bot)
        SpiceBot.channels.channel_list_request(bot)
        bot.osd(["[SpiceBot_Channels]", "I am now updating the channel listing for this server."])
        while SpiceBot.channels.channel_lock:
            pass
        SpiceBot.channels.join_all_channels(bot)
        foundchannelcount = len(list(SpiceBot.channels.chandict.keys()))
        bot.osd("[SpiceBot_Channels]", "Channel listing finished!", str(foundchannelcount) + " channel(s) found.")
        SpiceBot.channels.bot_part_empty(bot)
        return

    elif commandused == 'topic':
        if not len(botcom.dict['args']):
            SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Channel name input missing.")
            return
        channel = spicemanip(botcom.dict['args'], 1)
        if not SpiceBot.inlist(channel.lower(), list(SpiceBot.channels.chandict.keys())):
            SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Channel name {} not valid.".format(channel))
            return
        channel = str(channel).lower()
        topic = SpiceBot.channels.chandict[channel]['topic']
        channelname = SpiceBot.channels.chandict[channel]['name']
        bot.osd("Topic for {}: {}".format(channelname, topic))
        return

    if commandused.upper() in ['OP', 'HOP', 'VOICE', 'OWNER', 'ADMIN']:
        if not len(botcom.dict['args']):
            if trigger.is_privmsg:
                SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Channel name required.")
                return
            else:
                channel = trigger.sender
        else:
            channel = spicemanip(botcom.dict['args'], 1)
            if not SpiceBot.inlist(channel.lower(), list(SpiceBot.channels.chandict.keys())):
                SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Channel name {} not valid.".format(channel))
                return
            if not SpiceBot.inlist(channel.lower(), list(bot.channels.keys())):
                SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "I need to be in {} to see nick privileges.".format(channel))
                return

        privlist = SpiceBot.channel_privs(bot, channel, commandused.upper())
        dispmsg = []
        if not len(privlist):
            dispmsg.append("There are no Channel " + commandused.upper() + "s for " + str(channel))
        else:
            oplist = spicemanip(privlist, 'andlist')
            dispmsg.append("Channel " + commandused.upper() + "s for " + str(channel) + "  are: " + oplist)
        bot.osd(dispmsg, trigger.nick, 'notice')
        return

    # Users List
    if commandused == 'users':
        channel = spicemanip(botcom.dict['args'], 1)
        if not SpiceBot.inlist(channel.lower(), list(SpiceBot.channels.chandict.keys())):
            SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Channel name {} not valid.".format(channel))
            return
        if not SpiceBot.inlist(channel.lower(), list(bot.channels.keys())):
            SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "I need to be in {} to see user list.".format(channel))
            return
        dispmsg = []
        if not len(list(bot.channels[channel].privileges.keys())):
            dispmsg.append("There are no Channel users for " + str(channel))
        else:
            userslist = spicemanip(list(bot.channels[channel].privileges.keys()), 'andlist')
            dispmsg.append("Channel users for " + str(channel) + " are: " + userslist)
        bot.osd(dispmsg, trigger.nick, 'notice')
        return
