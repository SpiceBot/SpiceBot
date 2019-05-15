# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module


@sopel.module.rule(r'(?i)(Fuck|Screw) (you|off),? $nickname[ \t]*$')
def bot_command_srewyou(bot, trigger):
    bot.osd("Watch your mouth, " + trigger.nick + ", or I'll tell your mother!")
