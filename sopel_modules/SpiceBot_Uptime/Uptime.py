# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import time

from sopel_modules.SpiceBot_SBTools import humanized_time

from sopel_modules.SpiceBot_Logs import bot_logging


def configure(config):
    pass


def setup(bot):
    if 'SpiceBot_Uptime' not in bot.memory:
        now = time.time()
        bot_logging(bot, 'SpiceBot_Uptime', "Start time set to " + str(time.time()))
        bot.memory["SpiceBot_Uptime"] = now


@sopel.module.nickname_commands('uptime')
def bot_command_srewyou(bot, trigger):
    timesince = str(humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])) + " ago."
    bot.osd("I have been running since " + timesince)
