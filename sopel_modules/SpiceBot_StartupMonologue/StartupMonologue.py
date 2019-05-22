# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


def setup(bot):
    SpiceBot.logs.log('SpiceBot_StartupMonologue', "Starting setup procedure")
    SpiceBot.events.startup_add([SpiceBot.events.BOT_STARTUPMONOLOGUE_CHANNELS, SpiceBot.events.BOT_STARTUPMONOLOGUE_COMMANDSQUERY])  # ,SpiceBot.events.BOT_STARTUPMONOLOGUE_CONNECTED])

    if 'SpiceBot_StartupMonologue' not in bot.memory:
        bot.memory['SpiceBot_StartupMonologue'] = []
