# coding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
import sopel.tools
import sopel.config

import sopel_modules.SpiceBot as SpiceBot


def setup(bot):
    SpiceBot.botlogs.log('SpiceBot_Logs', "Starting Setup Procedure")
    SpiceBot.botevents.startup_add([SpiceBot.botevents.BOT_LOGS])
    SpiceBot.botevents.trigger(bot, SpiceBot.botevents.BOT_LOGS, "SpiceBot_Logs")


@sopel.module.event(SpiceBot.botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):

    if bot.config.core.logging_channel:
        channel = bot.config.core.logging_channel
        if channel not in bot.channels.keys():
            bot.write(('JOIN', bot.nick, channel))
            if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                bot.write(('SAJOIN', bot.nick, channel))

        while True:
            if len(SpiceBot.botlogs.SpiceBot_Logs["queue"]):
                bot.say(str(SpiceBot.botlogs.SpiceBot_Logs["queue"][0]), channel)
                del SpiceBot.botlogs.SpiceBot_Logs["queue"][0]
    else:
        SpiceBot.botlogs.sopel_config["logging_channel"] = False
        SpiceBot.botlogs.SpiceBot_Logs["queue"] = []
