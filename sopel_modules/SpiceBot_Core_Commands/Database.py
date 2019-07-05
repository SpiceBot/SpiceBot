# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Database
"""

# sopel imports
import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('database')
def bot_command_database(bot, trigger, botcom):
    bot.osd("Database is " + SpiceBot.config.db_type)
