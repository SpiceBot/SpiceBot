# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module


@sopel.module.rule(r'(?i)(Damnit|Lazy)? $nickname[ \t]*$')
def bot_command_damnlazy(bot, trigger):
    bot.osd("I do not tell you how to do your job, " + trigger.nick + "!!!")


@sopel.module.rule('$nickname is lazy')
def bot_command_damnlazy_b(bot, trigger):
    bot_command_damnlazy(bot, trigger)
