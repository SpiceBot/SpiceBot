# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents


def setup(bot):
    botlogs.log('SpiceBot_StartupMonologue', "Starting setup procedure")
    botevents.startup_add([botevents.BOT_STARTUPMONOLOGUE_CHANNELS, botevents.BOT_STARTUPMONOLOGUE_COMMANDSQUERY])  # , botevents.BOT_STARTUPMONOLOGUE_CONNECTED])

    if 'SpiceBot_StartupMonologue' not in bot.memory:
        bot.memory['SpiceBot_StartupMonologue'] = []
