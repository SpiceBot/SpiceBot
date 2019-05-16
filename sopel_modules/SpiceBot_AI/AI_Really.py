# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip


@sopel.module.rule(r'(?i)(really),? $nickname\?')
def bot_command_really(bot, trigger):
    really = spicemanip.main(["Yes, really.", "Really really"], "random")
    bot.reply(really)


@sopel.module.rule('$nickname really\?')
def bot_command_really_b(bot, trigger):
    bot_command_really(bot, trigger)
