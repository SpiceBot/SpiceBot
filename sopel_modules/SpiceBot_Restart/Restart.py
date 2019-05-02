#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.tools import stderr
from sopel.config.types import StaticSection, ValidatedAttribute

import sopel_modules.osd

from sopel_modules.SpiceBot_SBTools import service_manip


@sopel.module.nickname_commands('restart')
def nickname_comand_chanstats(bot, trigger):

    if not trigger.admin:
        bot.say("You are not authorized to perform this function.")

    stderr("Recieved Command to update.")
    bot.osd("Received command from " + trigger.nick + " to restart. Be Back Soon!", bot.channels.keys())

    service_manip(bot, bot.nick, 'restart')
