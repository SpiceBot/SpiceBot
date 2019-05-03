# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module
from sopel.tools import stderr

import sopel_modules.osd


from sopel_modules.SpiceBot_Botevents.BotEvents import set_bot_event, check_bot_events

from sopel_modules.SpiceBot_CommandsQuery.CommandsQuery import commandsquery_register


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
    stderr("[SpiceBot_StartupMonologue] " + bot.nick + " is now starting. Please wait while I load my configuration.")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    startupcomplete = [bot.nick + " startup complete"]

    while not check_bot_events(bot, ["SpiceBot_CommandsQuery"]):
        pass

    availablecomsnum, availablecomsfiles = 0, 0

    for commandstype in bot.memory['SpiceBot_CommandsQuery'].keys():
        if commandstype.endswith("_count"):
            availablecomsfiles += bot.memory['SpiceBot_CommandsQuery'][commandstype]
        else:
            availablecomsnum += len(bot.memory['SpiceBot_CommandsQuery'][commandstype].keys())

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    stderr("[SpiceBot_StartupMonologue] " + "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    while not check_bot_events(bot, ["startup_complete"]):
        pass

    # Announce to chan, then handle some closing stuff
    bot.osd(startupcomplete, bot.channels.keys())
    stderr("[SpiceBot_StartupMonologue] " + bot.nick + " startup complete")

    set_bot_event(bot, "SpiceBot_StartupMonologue")


def startup_reconnect(bot, trigger):

    # Startup
    stderr("[SpiceBot_StartupMonologue] " + bot.nick + " has reconnected.")
    bot.osd(" has reconnected.", bot.channels.keys(), 'ACTION')
