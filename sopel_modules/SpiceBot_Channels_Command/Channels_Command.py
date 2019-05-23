# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOADED])
@SpiceBot.prerun.prerun('nickname_command')
@sopel.module.nickname_commands('channels', 'channel')
def nickname_comand_channels(bot, trigger):

    if not len(trigger.sb['args']):
        commandused = 'list'
    else:
        commandused = spicemanip.main(trigger.sb['args'], 1).lower()

    trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')

    if commandused == 'list':
        chanlist = spicemanip.main(bot.channels.keys(), 'andlist')
        bot.osd("You can find me in " + chanlist)
        return

    elif commandused == 'total':
        botcount = len(bot.channels.keys())
        servercount = len(SpiceBot.channels.dict['list'].keys())
        bot.osd("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")
        return

    elif commandused == 'random':
        channel = spicemanip.main(SpiceBot.channels.dict['list'], 'random')
        topic = SpiceBot.channels.dict['list'][channel]['topic']
        msg = ["Random channel for you: {}.".format(SpiceBot.channels.dict['list'][channel]['name'])]
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
        SpiceBot.channels.bot_part_empty(bot)
        SpiceBot.channels.channel_list_request(bot)
        bot.osd(["[SpiceBot_Channels]", "I am now updating the channel listing for this server."])
        while SpiceBot.channels.channel_lock:
            pass
        SpiceBot.channels.join_all_channels(bot)
        foundchannelcount = len(SpiceBot.channels.dict['list'].keys())
        bot.osd("[SpiceBot_Channels]", "Channel listing finished!", str(foundchannelcount) + " channel(s) found.")
        SpiceBot.channels.bot_part_empty(bot)
        return

    elif commandused == 'topic':
        if not len(trigger.sb['args']):
            bot.osd("Channel name input missing.")
            return
        channel = spicemanip.main(trigger.sb['args'], 1)
        if not SpiceBot.inlist(channel.lower(), SpiceBot.channels.dict['list'].keys()):
            bot.osd("Channel name {} not valid.".format(channel))
            return
        topic = SpiceBot.channels.dict['list'][channel.lower()]['topic']
        channel = SpiceBot.channels.dict['list'][channel.lower()]['name']
        bot.osd("Topic for {}: {}".format(channel, topic))
        return

    if commandused.upper() in ['OP', 'HOP', 'VOICE', 'OWNER', 'ADMIN']:
        if not len(trigger.sb['args']):
            if trigger.is_privmsg:
                bot.osd("Channel name required.")
                return
            else:
                channel = trigger.sender
        else:
            channel = spicemanip.main(trigger.sb['args'], 1)
            if not SpiceBot.inlist(channel.lower(), SpiceBot.channels.dict['list'].keys()):
                bot.osd("Channel name {} not valid.".format(channel))
                return
            if not SpiceBot.inlist(channel.lower(), bot.channels.keys()):
                bot.osd("I need to be in {} to see nick privileges.".format(channel))
                return

        privlist = SpiceBot.channel_privs(bot, channel, commandused.upper())
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
        channel = spicemanip.main(trigger.sb['args'], 1)
        if not SpiceBot.inlist(channel.lower(), SpiceBot.channels.dict['list'].keys()):
            bot.osd("Channel name {} not valid.".format(channel))
            return
        if not SpiceBot.inlist(channel.lower(), bot.channels.keys()):
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
