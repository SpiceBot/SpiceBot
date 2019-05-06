#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

from sopel_modules.SpiceBot_SBTools import bot_logging, spicebot_reload


@sopel.module.nickname_commands('restart')
def nickname_comand_restart(bot, trigger):

    if not trigger.admin:
        bot.say("You are not authorized to perform this function.")

    quitmessage = "Received command from " + trigger.nick + " to restart. Be Back Soon!"
    bot_logging(bot, 'SpiceBot_Restart', quitmessage)
    bot.osd(quitmessage, bot.channels.keys())

    # service_manip(bot, bot.nick, 'restart', 'SpiceBot_Restart')
    spicebot_reload(bot, 'SpiceBot_Restart', quitmessage)
