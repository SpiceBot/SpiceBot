# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.trigger import PreTrigger

from .System import botevents
from sopel_modules.SpiceBot_SBTools import bot_logging

import time


@botevents.event('001')
@sopel.module.rule('.*')
def bot_startup_connection(bot, trigger):
    botevents.trigger(bot, botevents.BOT_WELCOME, "Welcome to the SpiceBot Events System")
    while not len(bot.channels.keys()) > 0:
        pass
    time.sleep(1)
    botevents.trigger(bot, botevents.BOT_CONNECTED, "Bot Connected to IRC")


@botevents.event(botevents.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_start(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    botevents.recieved(trigger)
    botevents.trigger(bot, botevents.BOT_READY, "Ready To Process module setup procedures")


@botevents.startup_check_ready()
@botevents.event(botevents.BOT_READY)
@sopel.module.rule('.*')
def bot_events_startup_complete(bot, trigger):
    botevents.trigger(bot, botevents.BOT_LOADED, "All registered modules setup procedures have completed")


@botevents.event(botevents.BOT_READY)
@sopel.module.rule('.*')
def bot_events_ready(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    botevents.recieved(trigger)


@botevents.event(botevents.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    botevents.recieved(trigger)
    while True:
        if len(botevents.SpiceBot_Events["trigger_queue"]):
            number = botevents.SpiceBot_Events["trigger_queue"][0]["number"]
            message = botevents.SpiceBot_Events["trigger_queue"][0]["message"]
            pretrigger = PreTrigger(
                bot.nick,
                ":SpiceBot_Events " + str(number) + " " + str(bot.nick) + " :" + message
            )
            bot.dispatch(pretrigger)
            del botevents.SpiceBot_Events["trigger_queue"][0]


@botevents.event(botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    botevents.recieved(trigger)
