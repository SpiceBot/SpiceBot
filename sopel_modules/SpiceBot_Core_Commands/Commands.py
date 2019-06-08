# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Commands system.

This Class stores commands in an easy to access manner
"""
import sopel

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.events.check_ready([SpiceBot.events.BOT_COMMANDS])
@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('commands', 'command')
def nickname_comand_commands(bot, trigger):

    if not len(trigger.sb['args']):
        commandused = 'list'
    else:
        commandused = spicemanip.main(trigger.sb['args'], 1).lower()

    commands_list = []
    for commandstype in SpiceBot.commands.dict['commands'].keys():
        if commandstype not in ['rule']:
            for com in SpiceBot.commands.dict['commands'][commandstype].keys():
                if com not in commands_list:
                    if commandstype in ['nickname']:
                        commands_list.append(bot.nick + " " + com)
                    else:
                        commands_list.append(com)

    if commandused == 'list':
        bot.osd(spicemanip.main(commands_list, 'andlist'), trigger.nick, 'NOTICE')
        return

    elif commandused == 'total':
        bot.osd("I have " + str(len(commands_list)) + " commands available.")
        return

    elif commandused == 'random':
        bot.osd(["Here's a random command for you:", spicemanip.main(commands_list, 'random')])
        return
