# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import time

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Tools import humanized_time


def setup(bot):
    if 'SpiceBot_Uptime' not in bot.memory:
        now = time.time()
        botlogs.log('SpiceBot_Uptime', "Start time set to " + str(time.time()))
        bot.memory["SpiceBot_Uptime"] = now


def shutdown(bot):
    if "SpiceBot_Uptime" in bot.memory:
        del bot.memory["SpiceBot_Uptime"]


@sopel.module.nickname_commands('uptime')
def bot_command_srewyou(bot, trigger):
    timesince = str(humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])) + " ago."
    bot.osd("I have been running since " + timesince)
