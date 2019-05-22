# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.botevents.BOT_COMMANDSQUERY)
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in SpiceBot.botcommands.SpiceBot_Commands['commands'].keys():
        availablecomsnum += len(SpiceBot.botcommands.SpiceBot_Commands['commands'][commandstype].keys())
    availablecomsfiles += SpiceBot.botcommands.SpiceBot_Commands['counts']

    bot.memory['SpiceBot_StartupMonologue'].append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    SpiceBot.botlogs.log('SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    SpiceBot.botevents.trigger(bot, SpiceBot.botevents.BOT_STARTUPMONOLOGUE_COMMANDSQUERY, "SpiceBot_StartupMonologue")
