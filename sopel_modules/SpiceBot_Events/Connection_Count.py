# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Events import botevents


@sopel.module.event(botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_startup_welcome(bot, trigger):
    botevents.SpiceBot_Events["RPL_WELCOME_Count"] += 1
    botevents.trigger(bot, botevents.BOT_RECONNECTED, "Bot Connected to IRC")
