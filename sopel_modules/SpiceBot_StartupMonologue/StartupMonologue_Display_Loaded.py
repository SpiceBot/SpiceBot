# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import time


@sopel.module.event(SpiceBot.events.BOT_LOADED)
@sopel.module.rule('.*')
def bot_startup_monologue_display(bot, trigger):

    if SpiceBot.events.dict["RPL_WELCOME_Count"] == 1:
        timesince = SpiceBot.humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])
        SpiceBot.bot.memory['SpiceBot_StartupMonologue'].append("Startup took " + timesince)

    # Announce to chan, then handle some closing stuff
    SpiceBot.logs.log('SpiceBot_StartupMonologue', bot.nick + " startup complete")
    bot.memory['SpiceBot_StartupMonologue'].insert(0, " startup complete")

    bot.osd(bot.memory['SpiceBot_StartupMonologue'], bot.channels.keys(), 'ACTION')

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE, "SpiceBot_StartupMonologue")
    SpiceBot.logs.log('SpiceBot_StartupMonologue', "Startup Monologue has been issued to all channels.", True)
