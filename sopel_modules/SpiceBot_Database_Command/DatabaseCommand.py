#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module


@sopel.module.nickname_commands('database')
def bot_command_gender(bot, trigger):
    bot.osd("Database is " + bot.config.core.db_type)
