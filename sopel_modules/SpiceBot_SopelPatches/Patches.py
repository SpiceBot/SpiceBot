#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel
import sopel.module

import sopel_modules.SpiceBot as SpiceBot


def setup(bot):

    SpiceBot.botlogs.log('Sopel_Patch', "Patching Sopels built-in url_callbacks")
    if 'url_callbacks' not in bot.memory:
        bot.memory['url_callbacks'] = sopel.tools.SopelMemory()

    SpiceBot.botlogs.log('Sopel_Patch', "Removing Stock Modules and verifying Dummy Command is present.")
    SpiceBot.stock_modules_begone(bot)
