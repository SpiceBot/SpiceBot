# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Events import botevents


@sopel.module.event(botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_startup_welcome(bot, trigger):
    """The Bot events system does not start until RPL_WELCOME 001 is recieved
    from the server"""
    botevents.trigger(bot, botevents.BOT_WELCOME, "Welcome to the SpiceBot Events System")
