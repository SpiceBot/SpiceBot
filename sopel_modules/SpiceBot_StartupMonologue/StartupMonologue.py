# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_Events.System import bot_events_recieved, bot_events_trigger
from sopel_modules.SpiceBot_LoadOrder.LoadOrder import set_bot_event
from sopel_modules.SpiceBot_SBTools import humanized_time, bot_logging
import time


def setup(bot):
    bot_logging(bot, 'SpiceBot_StartupMonologue', "Starting setup procedure")

    if 'SpiceBot_StartupMonologue' not in bot.memory:
        bot.memory['SpiceBot_StartupMonologue'] = []


@sopel.module.event('1003')
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):

    # Startup
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    bot.memory['SpiceBot_StartupMonologue'].append(bot.nick + " startup complete")


@sopel.module.event('2002')
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        availablecomsnum += len(bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype].keys())
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['counts'].keys():
        availablecomsfiles += bot.memory['SpiceBot_CommandsQuery']['counts'][commandstype]

    bot.memory['SpiceBot_StartupMonologue'].append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    bot_logging(bot, 'SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")


@sopel.module.event('2001')
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):

    botcount = len(bot.channels.keys())
    servercount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
    bot.memory['SpiceBot_StartupMonologue'].append("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")


@sopel.module.event('1004')
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):

    timesince = humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])
    bot.memory['SpiceBot_StartupMonologue'].append("Startup took " + timesince)

    # Announce to chan, then handle some closing stuff
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.osd(bot.memory['SpiceBot_StartupMonologue'], bot.channels.keys())

    set_bot_event(bot, "SpiceBot_StartupMonologue")
    bot_events_trigger(bot, 2005, "SpiceBot_StartupMonologue")


@sopel.module.event('2005')
@sopel.module.rule('.*')
def bot_events_setup(bot, trigger):
    bot_events_recieved(bot, trigger.event)
