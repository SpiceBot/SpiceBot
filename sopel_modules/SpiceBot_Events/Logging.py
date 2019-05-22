# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.botevents.BOT_WELCOME, SpiceBot.botevents.BOT_READY, SpiceBot.botevents.BOT_CONNECTED, SpiceBot.botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    """This is here simply to log to stderr that this was recieved."""
    SpiceBot.botlogs.log('SpiceBot_Events', trigger.args[1], True)
