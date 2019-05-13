# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module


@sopel.module.rule(r'(?i)(ping),? $nickname[ \t]*$')
def bot_command_ping(bot, trigger):
    bot.say("Pong")


@sopel.module.nickname_commands('ping')
def bot_command_ping_b(bot, trigger):
    bot_command_ping(bot, trigger)
