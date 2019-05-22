# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.nickname_commands('action')
def bot_command_action(bot, trigger):
    bot_command_process(bot, trigger)


@sopel.module.nickname_commands('notice')
def bot_command_notice(bot, trigger):
    bot_command_process(bot, trigger)


@sopel.module.nickname_commands('privmsg', 'say', 'msg')
def bot_command_privmsg(bot, trigger):
    bot_command_process(bot, trigger)


def bot_command_process(bot, trigger):

    if not SpiceBot.command_permissions_check(bot, trigger, ['admins', 'owner']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = SpiceBot.sopel_triggerargs(bot, trigger, 'nickname_command')

    if triggercommand in ['say', 'msg']:
        triggercommand = 'privmsg'

    if not len(triggerargs):
        bot.say("You must specify a channel or nick.")
        return

    target = spicemanip.main(triggerargs, 1)
    if (target not in ['allchans', 'allnicks']
            and not SpiceBot.inlist(target.lower(), SpiceBot.botchannels.SpiceBot_Channels['list'].keys())
            and not SpiceBot.inlist(target.lower(), bot.users)):
        bot.osd("Channel/nick name {} not valid.".format(target))
        return

    triggerargs = spicemanip.main(triggerargs, '2+', 'list')

    if target == 'allchans':
        targetsendlist = bot.channels.keys()
    elif target == 'allnicks':
        targetsendlist = bot.users
    else:
        targetsendlist = [target]

    botmessage = spicemanip.main(triggerargs, 0)
    if not botmessage:
        bot.say("You must specify a message to send.")
        return

    bot.osd(botmessage, targetsendlist, triggercommand.upper())
