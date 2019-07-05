# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Commands system.

This Class stores commands in an easy to access manner
"""
import sopel

import sopel_modules.spicemanip as spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('query')
def query_trigger(bot, trigger, botcom):
    bot.osd("I have been programmed to help find new commands by using `?`.")


@SpiceBot.prerun_query('nickname', 'nickname')
@sopel.module.nickname_commands('(.*)')
def query_detection_nick(bot, trigger, botcom):

    # command issued, check if valid
    if not botcom.dict['com'] or not len(botcom.dict['com']):
        return

    if not botcom.dict['com'][0] == bot.config.SpiceBot_Commands.query_prefix:
        return
    botcom.dict['com'] = botcom.dict['com'][1:]

    if not SpiceBot.letters_in_string(botcom.dict['com']):
        return

    commands_list = dict()
    for com in list(SpiceBot.commands.dict['commands']['nickname'].keys()):
        if com not in list(commands_list.keys()):
            commands_list[com] = SpiceBot.commands.dict['commands']['nickname'][com]

    if botcom.dict['com'].endswith("+"):

        botcom.dict['com'] = botcom.dict['com'][:-1]
        if not botcom.dict['com'] or not len(botcom.dict['com']):
            return

        if botcom.dict['com'].lower() not in list(commands_list.keys()):
            dispmsg = ["Cannot find any alias " + bot.nick + " commands: No valid commands match " + str(botcom.dict['com']) + "."]
            closestmatches = SpiceBot.similar_list(botcom.dict['com'], list(commands_list.keys()), 10, 'reverse')
            if len(closestmatches):
                dispmsg.append("The following " + bot.nick + " commands match " + str(botcom.dict['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".")
            bot.osd(dispmsg, trigger.nick, 'notice')
            return

        realcom = botcom.dict['com']
        if "aliasfor" in list(commands_list[botcom.dict['com']].keys()):
            realcom = commands_list[botcom.dict['com']]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.osd("The following " + bot.nick + " commands match " + str(botcom.dict['com']) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick, 'notice')
        return

    if botcom.dict['com'].endswith(bot.config.SpiceBot_Commands.query_prefix):

        botcom.dict['com'] = botcom.dict['com'][:-1]
        if not botcom.dict['com'] or not len(botcom.dict['com']):
            return

        closestmatches = SpiceBot.similar_list(botcom.dict['com'], list(commands_list.keys()), 10, 'reverse')
        if not len(closestmatches):
            bot.osd("Cannot find any similar " + bot.nick + " commands for " + str(botcom.dict['com']) + ".", trigger.nick, 'notice')
        else:
            bot.osd("The following " + bot.nick + " commands may match " + str(botcom.dict['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick, 'notice')
        return

    commandlist = []
    for command in list(commands_list.keys()):
        if command.lower().startswith(str(botcom.dict['com']).lower()):
            commandlist.append(command)

    if not len(commandlist):
        bot.osd("No " + bot.nick + " commands start with " + str(botcom.dict['com']) + ".", trigger.nick, 'notice')
    else:
        bot.osd("The following " + bot.nick + " commands start with " + str(botcom.dict['com']) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick, 'notice')


@SpiceBot.prerun_query('module', 'module')
@sopel.module.rule('^\?(.*)')
def query_detection(bot, trigger, botcom):

    # command issued, check if valid
    if not botcom.dict['com'] or not len(botcom.dict['com']):
        return

    if not SpiceBot.letters_in_string(botcom.dict['com']):
        return

    commands_list = dict()
    for commandstype in list(SpiceBot.commands.dict['commands'].keys()):
        if commandstype not in ['rule', 'nickname']:
            for com in list(SpiceBot.commands.dict['commands'][commandstype].keys()):
                if com not in list(commands_list.keys()):
                    commands_list[com] = SpiceBot.commands.dict['commands'][commandstype][com]

    if botcom.dict['com'][:-1] == "+":

        botcom.dict['com'] = botcom.dict['com'][:-1]
        if not botcom.dict['com'] or not len(botcom.dict['com']):
            return

        if botcom.dict['com'].lower() not in list(commands_list.keys()):
            dispmsg = ["Cannot find any alias commands: No valid commands match " + str(botcom.dict['com']) + "."]
            closestmatches = SpiceBot.similar_list(botcom.dict['com'], list(commands_list.keys()), 10, 'reverse')
            if len(closestmatches):
                dispmsg.append("The following commands match " + str(botcom.dict['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".")
            bot.osd(dispmsg, trigger.nick, 'notice')
            return

        realcom = botcom.dict['com']
        if "aliasfor" in list(commands_list[botcom.dict['com']].keys()):
            realcom = commands_list[botcom.dict['com']]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.osd("The following commands match " + str(botcom.dict['com']) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick, 'notice')
        return

    if botcom.dict['com'][:-1] == "?":

        botcom.dict['com'] = botcom.dict['com'][:-1]
        if not botcom.dict['com'] or not len(botcom.dict['com']):
            return

        closestmatches = SpiceBot.similar_list(botcom.dict['com'], list(commands_list.keys()), 10, 'reverse')
        if not len(closestmatches):
            bot.osd("Cannot find any similar commands for " + str(botcom.dict['com']) + ".", trigger.nick, 'notice')
        else:
            bot.osd("The following commands may match " + str(botcom.dict['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick, 'notice')
        return

    commandlist = []
    for command in list(commands_list.keys()):
        if command.lower().startswith(str(botcom.dict['com']).lower()):
            commandlist.append(command)

    if not len(commandlist):
        bot.osd("No commands start with " + str(botcom.dict['com']) + ".", trigger.nick, 'notice')
    else:
        bot.osd("The following commands start with " + str(botcom.dict['com']) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick, 'notice')
