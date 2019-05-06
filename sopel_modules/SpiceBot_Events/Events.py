# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from .System import bot_events_trigger, bot_events_recieved, bot_events_startup_check, bot_events_check
from sopel_modules.SpiceBot_SBTools import bot_logging

import time


@sopel.module.event('001')
@sopel.module.rule('.*')
def bot_startup_connection(bot, trigger):
    bot_events_trigger(bot, 1001, "Welcome to the SpiceBot Events System")

    if bot_events_check(bot, '1004'):
        return

    while not len(bot.channels.keys()) > 0:
        pass
    time.sleep(1)
    bot_events_trigger(bot, 1003, "Bot Connected to IRC")


@sopel.module.event('1001')
@sopel.module.rule('.*')
def bot_events_start(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1])
    bot_events_recieved(bot, trigger.event)

    bot_events_trigger(bot, 1002, "Ready To Process module setup procedures")

    while not bot_events_startup_check(bot):
        pass
    bot_events_trigger(bot, 1004, "All registered modules setup procedures have completed")


@sopel.module.event('1002')
@sopel.module.rule('.*')
def bot_events_ready(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1])
    bot_events_recieved(bot, trigger.event)


@sopel.module.event('1003')
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1])
    bot_events_recieved(bot, trigger.event)


@sopel.module.event('1004')
@sopel.module.rule('.*')
def bot_events_monologue(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1])
    bot_events_recieved(bot, trigger.event)
    bot.osd(trigger.args[1], bot.channels.keys())
