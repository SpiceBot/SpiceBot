# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_startup_welcome(bot, trigger):
   SpiceBot.events.dict["RPL_WELCOME_Count"] += 1
   if SpiceBot.events.dict["RPL_WELCOME_Count"] > 1:
       SpiceBot.events.trigger(bot, SpiceBot.events.BOT_RECONNECTED, "Bot ReConnected to IRC")
