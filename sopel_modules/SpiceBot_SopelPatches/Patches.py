#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel
import sopel.module

from sopel_modules.SpiceBot_Logs.Logs import botlogs
from sopel_modules.SpiceBot_SBTools import stock_modules_begone


def setup(bot):

    botlogs.log('Sopel_Patch', "Patching Sopels built-in url_callbacks")
    if 'url_callbacks' not in bot.memory:
        bot.memory['url_callbacks'] = sopel.tools.SopelMemory()

    botlogs.log('Sopel_Patch', "Removing Stock Modules and verifying Dummy Command is present.")
    stock_modules_begone(bot)
