# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot StartupMonologue system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot

import time


@sopel.module.event(SpiceBot.events.BOT_CHANNELS)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):
    # Startup
    SpiceBot.logs.log('SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", list(bot.channels.keys()), 'ACTION')
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_CONNECTED, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_startup_monologue_sopel_version(bot, trigger):
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_VERSION, "SpiceBot_StartupMonologue")
    SpiceBot.startupmonologue.dict["sopel_version"] = "Sopel " + str(SpiceBot.version.sopel["version_local_num"])
    SpiceBot.startupmonologue.dict["spicebot_version"] = "SpiceBot " + str(SpiceBot.version.spicebot["version_local_num"])


@sopel.module.event(SpiceBot.events.BOT_CHANNELS)
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):
    botcount = SpiceBot.channels.total_bot_channels()
    servercount = SpiceBot.channels.total_channels()
    displayval = "I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server."
    SpiceBot.startupmonologue.dict["channels"] = displayval
    SpiceBot.logs.log('SpiceBot_StartupMonologue', displayval)
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_CHANNELS, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_COMMANDS)
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):
    availablecomsnum, availablecomsfiles = 0, []
    for commandstype in list(SpiceBot.commands.dict['commands'].keys()):
        availablecomsnum += len(list(SpiceBot.commands.dict['commands'][commandstype].keys()))
        for validcom in list(SpiceBot.commands.dict['commands'][commandstype].keys()):
            if "filepath" in list(SpiceBot.commands.dict['commands'][commandstype][validcom].keys()):
                filepath = SpiceBot.commands.dict['commands'][commandstype][validcom]["filepath"].lower()
                if filepath not in availablecomsfiles:
                    availablecomsfiles.append(filepath)
    availablecomsfiles = len(availablecomsfiles)
    displayval = "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files."
    SpiceBot.startupmonologue.dict["commands"] = displayval
    SpiceBot.logs.log('SpiceBot_StartupMonologue', displayval)
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_COMMANDS, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_AI)
@sopel.module.rule('.*')
def bot_startup_monologue_ai(bot, trigger):
    availablecomsnum = SpiceBot.botai.dict['patterncounts']
    availablecomsfiles = SpiceBot.botai.dict['filecounts']
    displayval = "There are " + str(availablecomsnum) + " AI pattern matches available in " + str(availablecomsfiles) + " files."
    SpiceBot.startupmonologue.dict["ai"] = displayval
    SpiceBot.logs.log('SpiceBot_StartupMonologue', displayval)
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_AI, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_READY)
@sopel.module.rule('.*')
def bot_startup_monologue_releasenotes(bot, trigger):
    newnotes = False
    for notefile in list(SpiceBot.releasenotes.notes.keys()):
        if len(SpiceBot.releasenotes.notes[notefile]["new"]):
            newnotes = True
    if newnotes:
        displayval = "Check Release Notes for News"
        SpiceBot.startupmonologue.dict["releasenotes"] = displayval
        SpiceBot.logs.log('SpiceBot_StartupMonologue', displayval)
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_RNOTES, "SpiceBot_StartupMonologue")


@sopel.module.event(SpiceBot.events.BOT_LOADED)
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):
    dispmsg = [" startup complete"]
    for messagekey in list(SpiceBot.startupmonologue.dict.keys()):
        dispmsg.append(SpiceBot.startupmonologue.dict[messagekey])
    if SpiceBot.events.dict["RPL_WELCOME_Count"] == 1:
        timesince = SpiceBot.humanized_time(time.time() - SpiceBot.events.BOT_UPTIME)
        if timesince == "just now":
            timesince = "1 second"
        dispmsg.append("Startup took " + timesince)
    # Announce to chan, then handle some closing stuff
    SpiceBot.logs.log('SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.osd(dispmsg, list(bot.channels.keys()), 'ACTION')
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
        bot.osd(searchphrasefound, list(bot.channels.keys()))
    else:
        SpiceBot.logs.log('SpiceBot_Logs', "No issues found at bot startup!", True)
