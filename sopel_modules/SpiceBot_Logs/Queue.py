# coding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
import sopel.tools
import sopel.config

import sopel_modules.SpiceBot as SpiceBot


def setup(bot):
    SpiceBot.logs.log('SpiceBot_Logs', "Starting Setup Procedure")
    SpiceBot.events.startup_add([SpiceBot.events.BOT_LOGS])
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_LOGS, "SpiceBot_Logs")


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):

    if SpiceBot.config.config.core.logging_channel:
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
