# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents


@sopel.module.event(botevents.BOT_WELCOME, botevents.BOT_READY, botevents.BOT_CONNECTED, botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    """This is here simply to log to stderr that this was recieved."""
    botlogs.log('SpiceBot_Events', trigger.args[1], True)
