# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents
from sopel_modules.SpiceBot.Commands import botcommands


@sopel.module.event(botevents.BOT_COMMANDSQUERY)
@sopel.module.rule('.*')
def bot_startup_monologue_commands(bot, trigger):

    availablecomsnum, availablecomsfiles = 0, 0
    for commandstype in botcommands.SpiceBot_Commands['commands'].keys():
        availablecomsnum += len(botcommands.SpiceBot_Commands['commands'][commandstype].keys())
    availablecomsfiles += botcommands.SpiceBot_Commands['counts']

    bot.memory['SpiceBot_StartupMonologue'].append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")
    botlogs.log('SpiceBot_StartupMonologue', "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_COMMANDSQUERY, "SpiceBot_StartupMonologue")
