# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_READY)
@sopel.module.rule('.*')
def bot_events_complete_ai(bot, trigger):

    SpiceBot.logs.log('SpiceBot_Commands', "Found " + str(SpiceBot.botai.dict['patterncounts']) + " AI pattern Matches.", True)

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_AI, "SpiceBot_AI")
