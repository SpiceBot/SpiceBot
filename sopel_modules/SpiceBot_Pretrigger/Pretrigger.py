#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel
from sopel import module
from sopel.tools import stderr

from sopel import coretasks
from sopel.trigger import PreTrigger, Trigger
from sopel.bot import SopelWrapper

def setup(bot):
    sopel.tools._events.events.SpiceBotdbb = '7777'


@module.event('7777')
@module.rule('.*')
def parse_event_spicebotdbb(bot, trigger):
    stderr("\n" + trigger.event + "    " + str(trigger.args) + "\n")


@module.event('001')
@module.rule('.*')
def bot_trigger_simulator(bot, trigger):
    bot_trigger_create(bot, 7777, "Welcome to the SpiceBot Test Event System!")

def bot_event_trigger_create(bot, number, message):

    pretrigger = PreTrigger(
        bot.nick,
        ":irc.spicebot.net " +  str(number) + " " + str(bot.nick) + " :" + message
    )
    bot.dispatch(pretrigger)
