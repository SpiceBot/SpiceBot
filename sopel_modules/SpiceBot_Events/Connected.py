# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_Connected(bot, trigger):
    """Here, we wait until we are in at least one channel"""
    while not len(bot.channels.keys()) > 0:
        pass
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_CONNECTED, "Bot Connected to IRC")
