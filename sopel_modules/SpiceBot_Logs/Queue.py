# coding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
import sopel.tools
import sopel.config

from sopel_modules.SpiceBot.Logs import botlogs


@sopel.module.event('001')
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):

    if bot.config.core.logging_channel:
        channel = bot.config.core.logging_channel
        if channel not in bot.channels.keys():
            bot.write(('JOIN', bot.nick, channel))
            if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                bot.write(('SAJOIN', bot.nick, channel))

        while True:
            if len(botlogs.SpiceBot_Logs["queue"]):
                bot.say(str(botlogs.SpiceBot_Logs["queue"][0]), channel)
                del botlogs.SpiceBot_Logs["queue"][0]
    else:
        botlogs.sopel_config["logging_channel"] = False
        botlogs.SpiceBot_Logs["queue"] = []
