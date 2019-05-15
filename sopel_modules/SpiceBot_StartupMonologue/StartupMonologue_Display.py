# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_Events.System import botevents
from sopel_modules.SpiceBot_SBTools import humanized_time, bot_logging

import time


@sopel.module.event(botevents.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):
    botevents.recieved(trigger)

    # Startup
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_CONNECTED, "SpiceBot_StartupMonologue")


@sopel.module.event(botevents.BOT_COMMANDSQUERY)
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):
    botevents.recieved(trigger)

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        availablecomsnum += len(bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype].keys())
    availablecomsfiles += bot.memory['SpiceBot_CommandsQuery']['counts']

    bot.memory['SpiceBot_StartupMonologue'].append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    bot_logging(bot, 'SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_COMMANDSQUERY, "SpiceBot_StartupMonologue")


@sopel.module.event(botevents.BOT_CHANNELS)
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):
    botevents.recieved(trigger)

    botcount = len(bot.channels.keys())
    servercount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
    bot.memory['SpiceBot_StartupMonologue'].append("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_CHANNELS, "SpiceBot_StartupMonologue")


@sopel.module.event(botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):
    botevents.recieved(trigger)

    timesince = humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])
    bot.memory['SpiceBot_StartupMonologue'].append("Startup took " + timesince)

    # Announce to chan, then handle some closing stuff
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.memory['SpiceBot_StartupMonologue'].insert(0, " startup complete")

    bot.osd(bot.memory['SpiceBot_StartupMonologue'], bot.channels.keys(), 'ACTION')

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE, "SpiceBot_StartupMonologue")
    bot_logging(bot, 'SpiceBot_StartupMonologue', "Startup Monologue has been issued to all channels.", True)
