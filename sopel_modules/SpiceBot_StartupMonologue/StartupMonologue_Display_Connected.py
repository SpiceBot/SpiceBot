# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents


@sopel.module.event(botevents.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):

    # Startup
    botlogs.log('SpiceBot_StartupMonologue', bot.nick + " is now starting. Please wait while I load my configuration")
    bot.osd(" is now starting. Please wait while I load my configuration.", bot.channels.keys(), 'ACTION')

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_CONNECTED, "SpiceBot_StartupMonologue")
