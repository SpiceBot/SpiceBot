# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Events import botevents


@botevents.startup_check_ready()
@sopel.module.event(botevents.BOT_READY)
@sopel.module.rule('.*')
def bot_events_startup_complete(bot, trigger):
    """All events registered as required for startup have completed"""
    botevents.trigger(bot, botevents.BOT_LOADED, "All registered modules setup procedures have completed")
