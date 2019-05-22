# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel
import sopel.module

import sopel_modules.SpiceBot as SpiceBot


def setup(bot):
    SpiceBot.logs.log('SpiceBot_Commands', "Starting setup procedure")
    SpiceBot.events.startup_add([SpiceBot.events.BOT_COMMANDSQUERY])

    SpiceBot.commands.module_files_parse(bot)

    for comtype in ['module', 'nickname', 'rule']:
        SpiceBot.logs.log('SpiceBot_Commands', "Found " + str(len(SpiceBot.commands.dict['commands'][comtype].keys())) + " " + comtype + " commands.", True)

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_COMMANDSQUERY, "SpiceBot_Commands")


@sopel.module.event(SpiceBot.events.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):

    for comtype in SpiceBot.commands.dict['commands'].keys():
        if comtype not in ['module', 'nickname', 'rule']:
            SpiceBot.logs.log('SpiceBot_Commands', "Found " + str(len(SpiceBot.commands.dict['commands'][comtype].keys())) + " " + comtype + " commands.", True)
