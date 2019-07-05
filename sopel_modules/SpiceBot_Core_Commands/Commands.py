# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Commands system.

This Class stores commands in an easy to access manner
"""
import sopel

import spicemanip

import sopel_modules.SpiceBot as SpiceBot

# TODO commands sent in privmsg don't need bot.nick


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('commands', 'command')
def nickname_comand_commands(bot, trigger, botcom):

    if not len(botcom.dict['args']):
        commandused = 'list'
    else:
        commandused = spicemanip.main(botcom.dict['args'], 1).lower()

    if commandused == 'list':
        availablecomsnum, availablecomsfiles = 0, []
        for commandstype in list(SpiceBot.commands.dict['commands'].keys()):
            availablecomsnum += len(list(SpiceBot.commands.dict['commands'][commandstype].keys()))
            for validcom in list(SpiceBot.commands.dict['commands'][commandstype].keys()):
                if "filepath" in list(SpiceBot.commands.dict['commands'][commandstype][validcom].keys()):
                    filepath = SpiceBot.commands.dict['commands'][commandstype][validcom]["filepath"].lower()
                    if filepath not in availablecomsfiles:
                        availablecomsfiles.append(filepath)
        availablecomsfiles = len(availablecomsfiles)
        displayval = "There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files."
        bot.osd(displayval)
        return

    commands_list = []
    for commandstype in list(SpiceBot.commands.dict['commands'].keys()):
        if commandstype not in ['rule']:
            for com in list(SpiceBot.commands.dict['commands'][commandstype].keys()):
                if com not in commands_list:
                    if commandstype in ['nickname']:
                        commands_list.append(bot.nick + " " + com)
                    else:
                        commands_list.append(com)

    if commandused == 'total':
        bot.osd("I have " + str(len(commands_list)) + " commands available.")
        return

    if commandused == 'random':
        bot.osd(["Here's a random command for you:", spicemanip.main(commands_list, 'random')])
        return
