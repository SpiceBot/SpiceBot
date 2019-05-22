# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_COMMANDSQUERY)
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in SpiceBot.commands.dict['commands'].keys():
        availablecomsnum += len(SpiceBot.commands.dict['commands'][commandstype].keys())
    availablecomsfiles += SpiceBot.commands.dict['counts']

    bot.memory['SpiceBot_StartupMonologue'].append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    SpiceBot.logs.log('SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_COMMANDSQUERY, "SpiceBot_StartupMonologue")
