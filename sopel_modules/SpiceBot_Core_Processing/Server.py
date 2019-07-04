# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def server_name(bot, trigger):
    SpiceBot.server.rpl_welcome(trigger)


@sopel.module.event(SpiceBot.events.RPL_ISUPPORT)
@sopel.module.rule('.*')
def parse_event_005(bot, trigger):
    # SpiceBot.server.parse_reply_isupport(trigger)
    if trigger.args[-1] != 'are supported by this server':
        return
    SpiceBot.server.linenumber += 1
    parameters = trigger.args[1:-1]
    for param in parameters:
        if '=' in param:
            key, raw_value = param.split('=')
            if ',' in raw_value:
                settings = str(raw_value).split(',')
                for setting in settings:
                    bot.osd([str(key), "includes", str(setting)], "#deathbybandaid")
            else:
                bot.osd([str(key), "=", str(raw_value)], "#deathbybandaid")
