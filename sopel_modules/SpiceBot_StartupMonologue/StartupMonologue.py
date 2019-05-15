# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_Events.System import bot_events_recieved, bot_events_startup_register, botevents
from sopel_modules.SpiceBot_SBTools import bot_logging


def setup(bot):
    bot_logging(bot, 'SpiceBot_StartupMonologue', "Starting setup procedure")
    bot_events_startup_register(bot, [botevents.BOT_STARTUPMONOLOGUE_CHANNELS, botevents.BOT_STARTUPMONOLOGUE_COMMANDSQUERY, botevents.BOT_STARTUPMONOLOGUE_CONNECTED])

    if 'SpiceBot_StartupMonologue' not in bot.memory:
        bot.memory['SpiceBot_StartupMonologue'] = []


@sopel.module.event(botevents.BOT_STARTUPMONOLOGUE, botevents.BOT_STARTUPMONOLOGUE_CHANNELS, botevents.BOT_STARTUPMONOLOGUE_COMMANDSQUERY, botevents.BOT_STARTUPMONOLOGUE_CONNECTED)
@sopel.module.rule('.*')
def bot_events_setup(bot, trigger):
    bot_events_recieved(bot, trigger.event)
