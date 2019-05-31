# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Events system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_WELCOME, SpiceBot.events.BOT_READY, SpiceBot.events.BOT_CONNECTED, SpiceBot.events.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    """This is here simply to log to stderr that this was recieved."""
    SpiceBot.logs.log('SpiceBot_Events', trigger.args[1], True)


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):

    # Handling for connection count
    SpiceBot.events.dict["RPL_WELCOME_Count"] += 1
    if SpiceBot.events.dict["RPL_WELCOME_Count"] > 1:
        SpiceBot.events.trigger(bot, SpiceBot.events.BOT_RECONNECTED, "Bot ReConnected to IRC")
    else:
        SpiceBot.events.trigger(bot, SpiceBot.events.BOT_WELCOME, "Welcome to the SpiceBot Events System")

    """For items tossed in a queue, this will trigger them accordingly"""
    while True:
        if len(SpiceBot.events.dict["trigger_queue"]):
            pretriggerdict = SpiceBot.events.dict["trigger_queue"][0]
            SpiceBot.events.dispatch(bot, pretriggerdict)
            del SpiceBot.events.dict["trigger_queue"][0]


@sopel.module.event(SpiceBot.events.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_start(bot, trigger):
    """This stage is redundant, but shows the system is working."""
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_READY, "Ready To Process module setup procedures")

    """Here, we wait until we are in at least one channel"""
    while not len(bot.channels.keys()) > 0:
        pass
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_CONNECTED, "Bot Connected to IRC")


@SpiceBot.events.startup_check_ready()
@sopel.module.event(SpiceBot.events.BOT_READY)
@sopel.module.rule('.*')
def bot_events_startup_complete(bot, trigger):
    """All events registered as required for startup have completed"""
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_LOADED, "All registered modules setup procedures have completed")
