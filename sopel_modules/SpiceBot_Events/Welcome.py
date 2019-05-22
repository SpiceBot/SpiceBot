# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_startup_welcome(bot, trigger):
    """The Bot events system does not start until RPL_WELCOME 001 is recieved
    from the server"""
    if SpiceBot.events.check(SpiceBot.events.BOT_WELCOME):
        return
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_WELCOME, "Welcome to the SpiceBot Events System")
