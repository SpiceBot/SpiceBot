#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel
import sopel.module

from sopel_modules.SpiceBot_SBTools import bot_logging, stock_modules_begone

import os


def setup(bot):

    bot_logging(bot, 'Sopel_Patch', "Patching Sopels built-in url_callbacks")
    if 'url_callbacks' not in bot.memory:
        bot.memory['url_callbacks'] = sopel.tools.SopelMemory()

    bot_logging(bot, 'Sopel_Patch', "Removing Stock Modules and verifying Dummy Command is present.")
    stock_modules_begone(bot)
