# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Events import botevents


@sopel.module.event(botevents.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_Connected(bot, trigger):
    """Here, we wait until we are in at least one channel"""
    while not len(bot.channels.keys()) > 0:
        pass
    botevents.trigger(bot, botevents.BOT_CONNECTED, "Bot Connected to IRC")
