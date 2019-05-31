# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot StartupMonologue system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot

import time


@sopel.module.event(SpiceBot.events.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):
    # Startup
    SpiceBot.logs.log('SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_CONNECTED, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_CHANNELS)
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):
    botcount = len(bot.channels.keys())
    servercount = len(SpiceBot.channels.dict['list'].keys())
    displayval = "I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server."
    SpiceBot.startupmonologue.dict["channels"] = displayval
    SpiceBot.logs.log('SpiceBot_StartupMonologue', displayval)
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_CHANNELS, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_COMMANDS)
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):
    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in SpiceBot.commands.dict['commands'].keys():
        availablecomsnum += len(SpiceBot.commands.dict['commands'][commandstype].keys())
    availablecomsfiles += SpiceBot.commands.dict['counts']
    displayval = "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files."
    SpiceBot.startupmonologue.dict["commands"] = displayval
    SpiceBot.logs.log('SpiceBot_StartupMonologue', displayval)
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_COMMANDS, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_LOADED)
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):
    dispmsg = [" startup complete"]
    for messagekey in SpiceBot.startupmonologue.dict.keys():
        dispmsg.append(SpiceBot.startupmonologue.dict[messagekey])
    if SpiceBot.events.dict["RPL_WELCOME_Count"] == 1:
        timesince = SpiceBot.humanized_time(time.time() - SpiceBot.events.BOT_UPTIME)
        dispmsg.append("Startup took " + timesince)
    # Announce to chan, then handle some closing stuff
    SpiceBot.logs.log('SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.osd(dispmsg, bot.channels.keys(), 'ACTION')
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE, "SpiceBot_StartupMonologue")
    SpiceBot.logs.log('SpiceBot_StartupMonologue', "Startup Monologue has been issued to all channels.", True)


@sopel.module.event(SpiceBot.events.BOT_STARTUPMONOLOGUE)
@sopel.module.rule('.*')
def bot_startup_monologue_errors(bot, trigger):

    debuglines = SpiceBot.logs.stdio_logs_fetch()

    searchphrasefound = []
    for line in debuglines:
        if str(line).endswith("failed to load") and not str(line).startswith("0"):
            searchphrasefound.append(line)

    if len(searchphrasefound):
        for foundphase in searchphrasefound:
            SpiceBot.logs.log('SpiceBot_Logs', str(foundphase))
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        bot.osd(searchphrasefound, bot.channels.keys())
    else:
        SpiceBot.logs.log('SpiceBot_Logs', "No issues found at bot startup!", True)
