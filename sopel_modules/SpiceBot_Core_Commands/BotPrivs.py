# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('owners', 'owner')
def bot_command_owners(bot, trigger, botcom):
    bot_command_process(bot, trigger, botcom)


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('admins', 'admin')
def bot_command_admins(bot, trigger, botcom):
    bot_command_process(bot, trigger, botcom)


def bot_command_process(bot, trigger, botcom):

    if not botcom.dict['com'].endswith("s"):
        botcom.dict['com'] = str(botcom.dict['com'] + "s")

    privlist = spicemanip.main(SpiceBot.bot_privs(botcom.dict['com']), 'andlist')
    bot.osd(str(bot.nick) + " " + botcom.dict['com'] + ": " + privlist)
