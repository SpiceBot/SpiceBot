# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_Events.System import bot_events_recieved, bot_events_trigger
from sopel_modules.SpiceBot_SBTools import humanized_time, bot_logging
import time


@sopel.module.event('1003')
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    # Startup
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    bot_events_trigger(bot, 2012, "SpiceBot_StartupMonologue")


@sopel.module.event('2002')
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        availablecomsnum += len(bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype].keys())
    availablecomsfiles += bot.memory['SpiceBot_CommandsQuery']['counts']

    bot.memory['SpiceBot_StartupMonologue'].append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    bot_logging(bot, 'SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    bot_events_trigger(bot, 2011, "SpiceBot_StartupMonologue")


@sopel.module.event('2001')
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    botcount = len(bot.channels.keys())
    servercount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
    bot.memory['SpiceBot_StartupMonologue'].append("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")

    bot_events_trigger(bot, 2010, "SpiceBot_StartupMonologue")


@sopel.module.event('1004')
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    timesince = humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])
    bot.memory['SpiceBot_StartupMonologue'].append("Startup took " + timesince)

    # Announce to chan, then handle some closing stuff
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.memory['SpiceBot_StartupMonologue'].insert(0, " startup complete")

    bot.osd(bot.memory['SpiceBot_StartupMonologue'], bot.channels.keys(), 'ACTION')

    bot_events_trigger(bot, 2005, "SpiceBot_StartupMonologue")
    bot_logging(bot, 'SpiceBot_StartupMonologue', "Startup Monologue has been issued to all channels.", True)
