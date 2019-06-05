# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Logs system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):

    if SpiceBot.config.logging_channel:
        channel = bot.config.core.logging_channel
        if channel not in bot.channels.keys():
            bot.write(('JOIN', bot.nick, channel))
            if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                bot.write(('SAJOIN', bot.nick, channel))

        while True:
            if len(SpiceBot.logs.dict["queue"]):
                bot.osd(str(SpiceBot.logs.dict["queue"][0]), channel)
                del SpiceBot.logs.dict["queue"][0]
    else:
        SpiceBot.logs.dict["queue"] = []
