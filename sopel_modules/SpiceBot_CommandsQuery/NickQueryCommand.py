# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel
import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip


@SpiceBot.events.check_ready([SpiceBot.events.BOT_COMMANDSQUERY])
@SpiceBot.prerun.args('nickname_command')
@sopel.module.nickname_commands('(.*)')
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
    for com in SpiceBot.commands.dict['commands']['nickname'].keys():
        if com not in commands_list.keys():
            commands_list[com] = SpiceBot.commands.dict['commands']['nickname'][com]

    if trigger.sb['com'].endswith("+"):

        trigger.sb['com'] = trigger.sb['com'][:-1]
        if not trigger.sb['com'] or not len(trigger.sb['com']):
            return

        if trigger.sb['com'].lower() not in list(commands_list.keys()):
            dispmsg = ["Cannot find any alias " + bot.nick + " commands: No valid commands match " + str(trigger.sb['com']) + "."]
            closestmatches = SpiceBot.similar_list(bot, trigger.sb['com'], list(commands_list.keys()), 10, 'reverse')
            if len(closestmatches):
                dispmsg.append("The following " + bot.nick + " commands match " + str(trigger.sb['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".")
            bot.notice(dispmsg, trigger.nick)
            return

        realcom = trigger.sb['com']
        if "aliasfor" in commands_list[trigger.sb['com']].keys():
            realcom = commands_list[trigger.sb['com']]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.notice("The following " + bot.nick + " commands match " + str(trigger.sb['com']) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick)
        return

    if trigger.sb['com'].endswith("?"):

        trigger.sb['com'] = trigger.sb['com'][:-1]
        if not trigger.sb['com'] or not len(trigger.sb['com']):
            return

        closestmatches = SpiceBot.similar_list(bot, trigger.sb['com'], list(commands_list.keys()), 10, 'reverse')
        if not len(closestmatches):
            bot.notice("Cannot find any similar " + bot.nick + " commands for " + str(trigger.sb['com']) + ".", trigger.nick)
        else:
            bot.notice("The following " + bot.nick + " commands may match " + str(trigger.sb['com']) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick)
        return

    commandlist = []
    for command in list(commands_list.keys()):
        if command.lower().startswith(str(trigger.sb['com']).lower()):
            commandlist.append(command)

    if not len(commandlist):
        bot.notice("No " + bot.nick + " commands start with " + str(trigger.sb['com']) + ".", trigger.nick)
    else:
        bot.notice("The following " + bot.nick + " commands start with " + str(trigger.sb['com']) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
