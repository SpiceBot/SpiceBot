# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module


@sopel.module.rule('$nickname!')
def exclaim(bot, trigger):
    bot.say(trigger.nick + '!')


@sopel.module.rule('$nickname\?')
def imhere(bot, trigger):
    bot.say("I'm here, " + trigger.nick)
