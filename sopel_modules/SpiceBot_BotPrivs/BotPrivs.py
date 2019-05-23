# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.nickname_commands('owners', 'owner')
def bot_command_owners(bot, trigger):
    bot_command_process(bot, trigger)


@sopel.module.nickname_commands('admins')
def bot_command_admins(bot, trigger):
    bot_command_process(bot, trigger)


def bot_command_process(bot, trigger):
    triggerargs, triggercommand, command_type = SpiceBot.sopel_triggerargs(bot, trigger, 'nickname_command')

    if triggercommand == 'owner':
        triggercommand = 'owners'

    privlist = spicemanip.main(SpiceBot.bot_privs(bot, triggercommand), 'andlist')
    bot.osd(str(bot.nick) + " " + triggercommand + ": " + privlist)
