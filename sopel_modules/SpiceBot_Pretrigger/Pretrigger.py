#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel


@sopel.module.event('7777')
@sopel.module.rule('.*')
def parse_event_spicebotdbb(bot, trigger):
    sopel.tools.stderr("\n" + trigger.event + "    " + str(trigger.args) + "\n")


@sopel.module.event('001')
@sopel.module.rule('.*')
def bot_trigger_simulator(bot, trigger):
    bot_event_trigger_create(bot, 7777, "Welcome to the SpiceBot Test Event System!")


def bot_event_trigger_create(bot, number, message):
    pretrigger = sopel.trigger.PreTrigger(
        bot.nick,
        ":SpiceBot_Event " + str(number) + " " + str(bot.nick) + " :" + message
    )
    bot.dispatch(pretrigger)
