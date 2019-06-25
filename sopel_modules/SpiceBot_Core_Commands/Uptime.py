# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import time

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('uptime')
def bot_command_uptime(bot, trigger):
    timesince = str(SpiceBot.humanized_time(time.time() - SpiceBot.events.BOT_UPTIME)) + " ago."
    bot.osd("I have been running since " + timesince)
