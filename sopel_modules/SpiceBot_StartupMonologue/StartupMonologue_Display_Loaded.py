# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents
from sopel_modules.SpiceBot_SBTools import humanized_time

import time


@sopel.module.event(botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):

    if botevents.SpiceBot_Events["RPL_WELCOME_Count"] == 1:
        timesince = humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])
        bot.memory['SpiceBot_StartupMonologue'].append("Startup took " + timesince)

    # Announce to chan, then handle some closing stuff
    botlogs.log('SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.memory['SpiceBot_StartupMonologue'].insert(0, " startup complete")

    bot.osd(bot.memory['SpiceBot_StartupMonologue'], bot.channels.keys(), 'ACTION')

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE, "SpiceBot_StartupMonologue")
    botlogs.log('SpiceBot_StartupMonologue', "Startup Monologue has been issued to all channels.", True)
