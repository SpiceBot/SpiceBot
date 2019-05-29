# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('action')
def bot_command_action(bot, trigger):
    bot_command_process(bot, trigger)


@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('notice')
def bot_command_notice(bot, trigger):
    bot_command_process(bot, trigger)


@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('privmsg', 'say', 'msg')
def bot_command_privmsg(bot, trigger):
    bot_command_process(bot, trigger)


def bot_command_process(bot, trigger):

    if not SpiceBot.command_permissions_check(bot, trigger, ['admins', 'owner']):
        bot.osd("I was unable to process this Bot Nick command due to privilege issues.")
        return

    if trigger.sb['com'] in ['say', 'msg']:
        trigger.sb['com'] = 'privmsg'

    if not len(trigger.sb['args']):
        bot.osd("You must specify a channel or nick.")
        return

    target = spicemanip.main(trigger.sb['args'], 1)
    if (target not in ['allchans', 'allnicks']
            and not SpiceBot.inlist(target.lower(), SpiceBot.channels.dict['list'].keys())
            and not SpiceBot.inlist(target.lower(), bot.users)):
        bot.osd("Channel/nick name {} not valid.".format(target))
        return

    trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')

    if target == 'allchans':
        targetsendlist = bot.channels.keys()
    elif target == 'allnicks':
        targetsendlist = bot.users
    else:
        targetsendlist = [target]

    botmessage = spicemanip.main(trigger.sb['args'], 0)
    if not botmessage:
        bot.osd("You must specify a message to send.")
        return

    bot.osd(botmessage, targetsendlist, trigger.sb['com'].upper())
