# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module

from sopel_modules.SpiceBot_Botevents.BotEvents import set_bot_event, check_bot_events

from sopel_modules.SpiceBot_SBTools import humanized_time, bot_logging
import time


def configure(config):
    pass


def setup(bot):
    pass


@module.event('001')
@module.rule('.*')
@module.thread(True)
def bot_startup_monologue(bot, trigger):

    while not check_bot_events(bot, ["connected"]):
        pass

    if check_bot_events(bot, ["SpiceBot_StartupMonologue"]):
        startup_reconnect(bot, trigger)
    else:
        startup_fresh(bot, trigger)


def startup_fresh(bot, trigger):

    # Startup
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    startupcomplete = [bot.nick + " startup complete"]

    while not check_bot_events(bot, ["SpiceBot_CommandsQuery"]):
        pass

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        availablecomsnum += len(bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype].keys())
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['counts'].keys():
        availablecomsfiles += bot.memory['SpiceBot_CommandsQuery']['counts'][commandstype]

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    bot_logging(bot, 'SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    while not check_bot_events(bot, ["SpiceBot_Channels"]):
        pass

    botcount = len(bot.channels.keys())
    servercount = len(bot.memory['SpiceBot_Channels']['channels'].keys())
    startupcomplete.append("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")

    while not check_bot_events(bot, ["startup_complete"]):
        pass

    timesince = humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])
    startupcomplete.append("Startup took " + timesince)

    # Announce to chan, then handle some closing stuff
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.osd(startupcomplete, bot.channels.keys())

    set_bot_event(bot, "SpiceBot_StartupMonologue")


def startup_reconnect(bot, trigger):

    # Startup
    bot_logging(bot, 'SpiceBot_StartupMonologue', bot.nick + " has reconnected.")
    bot.osd(" has reconnected.", bot.channels.keys(), 'ACTION')
