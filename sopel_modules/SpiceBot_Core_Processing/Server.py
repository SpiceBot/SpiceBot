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
    SpiceBot.server.linenumber += 1
    bot.osd([str(SpiceBot.server.linenumber), str(trigger)], "deathbybandaid")
    # SpiceBot.server.parse_reply_isupport(trigger)
