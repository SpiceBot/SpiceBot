# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun.prerun('nickname_command')
@sopel.module.nickname_commands('owners', 'owner')
def bot_command_owners(bot, trigger):
    bot_command_process(bot, trigger)


@SpiceBot.prerun.prerun('nickname_command')
@sopel.module.nickname_commands('admins')
def bot_command_admins(bot, trigger):
    bot_command_process(bot, trigger)


def bot_command_process(bot, trigger):

    if trigger.sb['com'] == 'owner':
        trigger.sb['com'] = 'owners'

    privlist = spicemanip.main(SpiceBot.bot_privs(bot, trigger.sb['com']), 'andlist')
    bot.osd(str(bot.nick) + " " + trigger.sb['com'] + ": " + privlist)
