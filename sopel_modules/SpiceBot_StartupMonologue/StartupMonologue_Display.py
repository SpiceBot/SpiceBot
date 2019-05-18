# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents
from sopel_modules.SpiceBot.Channels import botchannels
from sopel_modules.SpiceBot_SBTools import humanized_time

import time


@sopel.module.event(botevents.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):

    # Startup
    botlogs.log('SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_CONNECTED, "SpiceBot_StartupMonologue")


@sopel.module.event(botevents.BOT_COMMANDSQUERY)
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        availablecomsnum += len(bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype].keys())
    availablecomsfiles += bot.memory['SpiceBot_CommandsQuery']['counts']

    bot.memory['SpiceBot_StartupMonologue'].append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    botlogs.log('SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_COMMANDSQUERY, "SpiceBot_StartupMonologue")


@sopel.module.event(botevents.BOT_CHANNELS)
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):

    botcount = len(bot.channels.keys())
    servercount = len(botchannels.SpiceBot_Channels['list'].keys())
    bot.memory['SpiceBot_StartupMonologue'].append("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_CHANNELS, "SpiceBot_StartupMonologue")


@sopel.module.event(botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):

    timesince = humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])
    bot.memory['SpiceBot_StartupMonologue'].append("Startup took " + timesince)

    # Announce to chan, then handle some closing stuff
    botlogs.log('SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.memory['SpiceBot_StartupMonologue'].insert(0, " startup complete")

    bot.osd(bot.memory['SpiceBot_StartupMonologue'], bot.channels.keys(), 'ACTION')

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE, "SpiceBot_StartupMonologue")
    botlogs.log('SpiceBot_StartupMonologue', "Startup Monologue has been issued to all channels.", True)
