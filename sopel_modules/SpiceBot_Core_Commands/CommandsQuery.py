# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Commands system.

This Class stores commands in an easy to access manner
"""
import sopel

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('query')
def query_trigger(bot, trigger):
    bot.osd("I have been programmed to help find new commands by using `?`.")


@SpiceBot.events.check_ready([SpiceBot.events.BOT_COMMANDS])
@SpiceBot.prerun_query('nickname', 'nickname')
@sopel.module.nickname_commands('^\?(.*)')
def query_detection_nick(bot, trigger):

    # command issued, check if valid
    if not trigger.sb['com'] or not len(trigger.sb['com']):
        return

    if not trigger.sb['com'][0] == "?":
        return
    trigger.sb['com'] = trigger.sb['com'][1:]

    if not SpiceBot.letters_in_string(trigger.sb['com']):
        return

    commands_list = dict()
    for com in list(SpiceBot.commands.dict['commands']['nickname'].keys()):
        if com not in list(commands_list.keys()):
            commands_list[com] = SpiceBot.commands.dict['commands']['nickname'][com]

    if trigger.sb['com'].endswith("+"):

        trigger.sb['com'] = trigger.sb['com'][:-1]
        if not trigger.sb['com'] or not len(trigger.sb['com']):
            return

        if trigger.sb['com'].lower() not in list(commands_list.keys()):
            dispmsg = ["Cannot find any alias " + bot.nick + " commands: No valid commands match " + str(trigger.sb['com']) + "."]
            closestmatches = SpiceBot.similar_list(trigger.sb['com'], list(commands_list.keys()), 10, 'reverse')
            if len(closestmatches):
                dispmsg.append("The following " + bot.nick + " commands match " + str(trigger.sb['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".")
            bot.osd(dispmsg, trigger.nick, 'notice')
            return

        realcom = trigger.sb['com']
        if "aliasfor" in list(commands_list[trigger.sb['com']].keys()):
            realcom = commands_list[trigger.sb['com']]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.osd("The following " + bot.nick + " commands match " + str(trigger.sb['com']) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick, 'notice')
        return

    if trigger.sb['com'].endswith("?"):

        trigger.sb['com'] = trigger.sb['com'][:-1]
        if not trigger.sb['com'] or not len(trigger.sb['com']):
            return

        closestmatches = SpiceBot.similar_list(trigger.sb['com'], list(commands_list.keys()), 10, 'reverse')
        if not len(closestmatches):
            bot.osd("Cannot find any similar " + bot.nick + " commands for " + str(trigger.sb['com']) + ".", trigger.nick, 'notice')
        else:
            bot.osd("The following " + bot.nick + " commands may match " + str(trigger.sb['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick, 'notice')
        return

    commandlist = []
    for command in list(commands_list.keys()):
        if command.lower().startswith(str(trigger.sb['com']).lower()):
            commandlist.append(command)

    if not len(commandlist):
        bot.osd("No " + bot.nick + " commands start with " + str(trigger.sb['com']) + ".", trigger.nick, 'notice')
    else:
        bot.osd("The following " + bot.nick + " commands start with " + str(trigger.sb['com']) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick, 'notice')


@SpiceBot.events.check_ready([SpiceBot.events.BOT_COMMANDS])
@SpiceBot.prerun_query('module', 'module')
@sopel.module.rule('^\?(.*)')
def query_detection(bot, trigger):

    # command issued, check if valid
    if not trigger.sb['com'] or not len(trigger.sb['com']):
        return

    if not SpiceBot.letters_in_string(trigger.sb['com']):
        return

    commands_list = dict()
    for commandstype in list(SpiceBot.commands.dict['commands'].keys()):
        if commandstype not in ['rule', 'nickname']:
            for com in list(SpiceBot.commands.dict['commands'][commandstype].keys()):
                if com not in list(commands_list.keys()):
                    commands_list[com] = SpiceBot.commands.dict['commands'][commandstype][com]

    if trigger.sb['com'][:-1] == "+":

        trigger.sb['com'] = trigger.sb['com'][:-1]
        if not trigger.sb['com'] or not len(trigger.sb['com']):
            return

        if trigger.sb['com'].lower() not in list(commands_list.keys()):
            dispmsg = ["Cannot find any alias commands: No valid commands match " + str(trigger.sb['com']) + "."]
            closestmatches = SpiceBot.similar_list(trigger.sb['com'], list(commands_list.keys()), 10, 'reverse')
            if len(closestmatches):
                dispmsg.append("The following commands match " + str(trigger.sb['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".")
            bot.osd(dispmsg, trigger.nick, 'notice')
            return

        realcom = trigger.sb['com']
        if "aliasfor" in list(commands_list[trigger.sb['com']].keys()):
            realcom = commands_list[trigger.sb['com']]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.osd("The following commands match " + str(trigger.sb['com']) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick, 'notice')
        return

    if trigger.sb['com'][:-1] == "?":

        trigger.sb['com'] = trigger.sb['com'][:-1]
        if not trigger.sb['com'] or not len(trigger.sb['com']):
            return

        closestmatches = SpiceBot.similar_list(trigger.sb['com'], list(commands_list.keys()), 10, 'reverse')
        if not len(closestmatches):
            bot.osd("Cannot find any similar commands for " + str(trigger.sb['com']) + ".", trigger.nick, 'notice')
        else:
            bot.osd("The following commands may match " + str(trigger.sb['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick, 'notice')
        return

    commandlist = []
    for command in list(commands_list.keys()):
        if command.lower().startswith(str(trigger.sb['com']).lower()):
            commandlist.append(command)

    if not len(commandlist):
        bot.osd("No commands start with " + str(trigger.sb['com']) + ".", trigger.nick, 'notice')
    else:
        bot.osd("The following commands start with " + str(trigger.sb['com']) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick, 'notice')
