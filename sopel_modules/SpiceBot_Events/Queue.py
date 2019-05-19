# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Events import botevents


@sopel.module.event(botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):
    """For items tossed in a queue, this will trigger them accordingly"""
    while True:
        if len(botevents.SpiceBot_Events["trigger_queue"]):
            pretriggerdict = botevents.SpiceBot_Events["trigger_queue"][0]
            botevents.dispatch(pretriggerdict)
            del botevents.SpiceBot_Events["trigger_queue"][0]
