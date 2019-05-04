# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.tools import stderr

import spicemanip

import time

from sopel_modules.SpiceBot_SBTools import humanized_time


def configure(config):
    pass


def setup(bot):
    bot.memory["SpiceBot_Uptime"] = time.time()


@sopel.module.nickname_commands('uptime')
def bot_command_srewyou(bot, trigger):
    timesince = str(humanized_time(time.time() - bot.memory["SpiceBot_Uptime"])) + " ago."
    bot.osd("I have been running since " + timesince)
