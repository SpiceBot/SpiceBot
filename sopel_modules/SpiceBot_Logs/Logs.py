# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

from sopel_modules.SpiceBot_SBTools import bot_logging
from sopel_modules.SpiceBot_Events.System import bot_events_startup_register, bot_events_recieved, bot_events_trigger
from sopel_modules.SpiceBot_LoadOrder.LoadOrder import set_bot_event, startup_bot_event


def configure(config):
    config.define_section("SpiceBot_Logs", SpiceBot_Logs_MainSection, validate=False)
    config.SpiceBot_Logs.configure_setting('logging_channel', 'SpiceBot_Logs channels')


class SpiceBot_Logs_MainSection(StaticSection):
    logging_channel = ValidatedAttribute('logging_channel', default=False)


def setup(bot):
    bot_logging(bot, 'SpiceBot_Logs', "Starting Setup Procedure")
    bot.config.define_section("SpiceBot_Logs", SpiceBot_Logs_MainSection, validate=False)

    bot_events_startup_register(bot, ['2004'])

    startup_bot_event(bot, "SpiceBot_CommandsQuery")

    if 'SpiceBot_Logs' not in bot.memory:
        bot.memory['SpiceBot_Logs'] = {"logs": {}, "queue": []}

    set_bot_event(bot, "SpiceBot_Logs")
    bot_events_trigger(bot, 2004, "SpiceBot_Logs")


def shutdown(bot):
    if "SpiceBot_Logs" in bot.memory:
        del bot.memory["SpiceBot_Logs"]


@sopel.module.event('1004')
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    if bot.config.SpiceBot_Logs.logging_channel:
        channel = bot.config.SpiceBot_Logs.logging_channel
        if channel not in bot.channels.keys():
            bot.write(('JOIN', bot.nick, channel))
            if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                bot.write(('SAJOIN', bot.nick, channel))

        if 'SpiceBot_Logs' not in bot.memory:
            bot.memory['SpiceBot_Logs'] = {"logs": {}, "queue": []}

        while 'SpiceBot_Logs' in bot.memory:
            if len(bot.memory['SpiceBot_Logs']["queue"]):
                bot.say(str(bot.memory['SpiceBot_Logs']["queue"][0]), channel)
                del bot.memory['SpiceBot_Logs']["queue"][0]


@sopel.module.event('2004')
@sopel.module.rule('.*')
def bot_events_setup(bot, trigger):
    bot_events_recieved(bot, trigger.event)
