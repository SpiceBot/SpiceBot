# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_Events.System import bot_events_recieved
from sopel_modules.SpiceBot_SBTools import bot_logging


def setup(bot):
    bot_logging(bot, 'SpiceBot_StartupMonologue', "Starting setup procedure")

    if 'SpiceBot_StartupMonologue' not in bot.memory:
        bot.memory['SpiceBot_StartupMonologue'] = []


@sopel.module.event('2005')
@sopel.module.rule('.*')
def bot_events_setup(bot, trigger):
    bot_events_recieved(bot, trigger.event)
