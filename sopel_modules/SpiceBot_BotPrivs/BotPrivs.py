# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, bot_privs


def configure(config):
    pass


def setup(bot):
    pass


@sopel.module.nickname_commands('owners', 'owners')
def bot_command_owners(bot, trigger):
    bot_command_process(bot, trigger)


@sopel.module.nickname_commands('admins')
def bot_command_admins(bot, trigger):
    bot_command_process(bot, trigger)


def bot_command_process(bot, trigger):
    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    if triggercommand == 'owner':
        triggercommand = 'owners'

    privlist = spicemanip.main(bot_privs(bot, triggercommand), 'andlist')
    bot.osd(str(bot.nick) + " " + triggercommand + ": " + privlist)
