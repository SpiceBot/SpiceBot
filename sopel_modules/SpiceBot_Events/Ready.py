# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_start(bot, trigger):
    """This stage is redundant, but shows the system is working."""
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_READY, "Ready To Process module setup procedures")
