#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

from sopel_modules.SpiceBot_SBTools import service_manip
from sopel_modules.SpiceBot_Logs import bot_logging


@sopel.module.nickname_commands('restart')
def nickname_comand_chanstats(bot, trigger):

    if not trigger.admin:
        bot.say("You are not authorized to perform this function.")

    bot_logging(bot, 'SpiceBot_Restart', "Received command from " + trigger.nick + " to restart")
    bot.osd("Received command from " + trigger.nick + " to restart. Be Back Soon!", bot.channels.keys())

    service_manip(bot, bot.nick, 'restart', 'SpiceBot_Restart')
