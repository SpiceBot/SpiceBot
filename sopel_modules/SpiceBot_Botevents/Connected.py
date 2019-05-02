# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module
from sopel.tools import stderr
from .BotEvents import check_bot_events, startup_bot_event, set_bot_event

import time


@module.event('001')
@module.rule('.*')
def bot_startup_connection(bot, trigger):

    if check_bot_events(bot, ["startup_complete"]):
        return
    startup_bot_event(bot, "connected")

    while not len(bot.channels.keys()) > 0:
        pass
    time.sleep(1)

    set_bot_event(bot, "connected")
