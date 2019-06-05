# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Modules system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_READY)
@sopel.module.rule('.*')
def bot_events_complete_modules(bot, trigger):

    for comtype in SpiceBot.commands.dict['commands'].keys():
        if comtype not in ['module', 'nickname', 'rule']:
            SpiceBot.logs.log('SpiceBot_Commands', "Found " + str(len(SpiceBot.commands.dict['commands'][comtype].keys())) + " " + comtype + " commands.", True)

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_COMMANDS, "SpiceBot_Commands")
