# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_startup_welcome(bot, trigger):
    """The Bot events system does not start until RPL_WELCOME 001 is recieved
    from the server"""
    if SpiceBot.botevents.check(SpiceBot.botevents.BOT_WELCOME):
        return
    SpiceBot.botevents.trigger(bot, SpiceBot.botevents.BOT_WELCOME, "Welcome to the SpiceBot Events System")
