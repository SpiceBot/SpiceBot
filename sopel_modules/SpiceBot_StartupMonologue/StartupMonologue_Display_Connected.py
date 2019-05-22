# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):

    # Startup
    SpiceBot.logs.log('SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_CONNECTED, "SpiceBot_StartupMonologue")
