# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.trigger import PreTrigger

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents

import time


def setup(bot):
    botlogs.log('SpiceBot_Events', "Starting setup procedure")


@sopel.module.event(botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_startup_welcome(bot, trigger):
    """The Bot events system does not start until RPL_WELCOME 001 is recieved
    from the server"""
    botevents.trigger(bot, botevents.BOT_WELCOME, "Welcome to the SpiceBot Events System")


@sopel.module.event(botevents.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_start(bot, trigger):
    """This stage is redundant, but shows the system is working."""
    botlogs.log('SpiceBot_Events', trigger.args[1], True)
    botevents.trigger(bot, botevents.BOT_READY, "Ready To Process module setup procedures")


@sopel.module.event(botevents.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_startup_connection(bot, trigger):
    """Here, we wait until we are in at least one channel"""
    while not len(bot.channels.keys()) and not botevents.check([botevents.BOT_CHANNELS]):
        pass
    time.sleep(1)
    botevents.trigger(bot, botevents.BOT_CONNECTED, "Bot Connected to IRC")


@botevents.startup_check_ready()
@sopel.module.event(botevents.BOT_READY)
@sopel.module.rule('.*')
def bot_events_startup_complete(bot, trigger):
    """All events registered as required for startup have completed"""
    botlogs.log('SpiceBot_Events', trigger.args[1], True)
    botevents.trigger(bot, botevents.BOT_LOADED, "All registered modules setup procedures have completed")


@sopel.module.event(botevents.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):
    """For items tossed in a queue, this will trigger them accordingly"""
    botlogs.log('SpiceBot_Events', trigger.args[1], True)

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
            botevents.recieved({"number": number, "message": message})
        else:
            if botevents.startup_check():
                return


@sopel.module.event(botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    """This is here simply to log to stderr that this was recieved."""
    botlogs.log('SpiceBot_Events', trigger.args[1], True)
