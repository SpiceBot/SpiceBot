# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.spicemanip import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('action')
def bot_command_action(bot, trigger, botcom):
    bot_command_process(bot, trigger, botcom)


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('notice')
def bot_command_notice(bot, trigger, botcom):
    bot_command_process(bot, trigger, botcom)


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('privmsg', 'say', 'msg')
def bot_command_privmsg(bot, trigger, botcom):
    bot_command_process(bot, trigger, botcom)


def bot_command_process(bot, trigger, botcom):

    if not SpiceBot.users.command_permissions_check(bot, trigger, ['admins', 'owner']):
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "I was unable to process this Bot Nick command due to privilege issues.")
        return

    if botcom.dict['com'] in ['say', 'msg']:
        botcom.dict['com'] = 'privmsg'

    if not len(botcom.dict['args']):
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "You must specify a channel or nick.")
        return

    target = spicemanip(botcom.dict['args'], 1)
    if (target not in ['allchans', 'allnicks']
            and not SpiceBot.channels.ischannel(target)
            and not SpiceBot.inlist(target.lower(), bot.users)):
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Channel/nick name {} not valid.".format(target))
        return

    botcom.dict['args'] = spicemanip(botcom.dict['args'], '2+', 'list')

    if target == 'allchans':
        targetsendlist = list(bot.channels.keys())
    elif target == 'allnicks':
        targetsendlist = bot.users
    else:
        targetsendlist = [target]

    botmessage = spicemanip(botcom.dict['args'], 0)
    if not botmessage:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "You must specify a message to send.")
        return

    bot.osd(botmessage, targetsendlist, botcom.dict['com'].upper())
