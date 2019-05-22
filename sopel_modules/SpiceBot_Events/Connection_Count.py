# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_startup_welcome(bot, trigger):
   SpiceBot.botevents.SpiceBot_Events["RPL_WELCOME_Count"] += 1
   if SpiceBot.botevents.SpiceBot_Events["RPL_WELCOME_Count"] > 1:
       SpiceBot.botevents.trigger(bot, SpiceBot.botevents.BOT_RECONNECTED, "Bot ReConnected to IRC")
