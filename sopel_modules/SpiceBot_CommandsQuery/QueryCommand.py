# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel
import sopel.module

from sopel_modules.SpiceBot_Events.System import bot_events_check
from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, similar_list, letters_in_string


import spicemanip


@sopel.module.rule('^\?(.*)')
def query_detection(bot, trigger):

    while not bot_events_check(bot, '2002'):
        pass

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'query_command')

    # command issued, check if valid
    if not triggercommand or not len(triggercommand):
        return

    if not letters_in_string(triggercommand):
        return

    commands_list = dict()
    for commandstype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        if commandstype != 'rule':
            for com in bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype].keys():
                if com not in commands_list.keys():
                    if commandstype == 'nickname':
                        commands_list[str(bot.nick) + " " + com] = bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype][com]
                        if "aliasfor" in commands_list[str(bot.nick) + " " + com].keys():
                            aliasforcom = commands_list[str(bot.nick) + " " + com]["aliasfor"]
                            commands_list[str(bot.nick) + " " + com]["aliasfor"] = str(bot.nick) + " " + aliasforcom
                    else:
                        commands_list[com] = bot.memory['SpiceBot_CommandsQuery']['commands'][commandstype][com]

    botnick_coms = list(bot.memory['SpiceBot_CommandsQuery']['commands']['nickname'].keys())
    # botnick_coms.extend(bot.memory['SpiceBot_CommandsQuery']['nickrules'])

    if triggercommand.lower().startswith(str(bot.nick).lower()):
        searchlist = botnick_coms
        searchitem = spicemanip.main([triggercommand].extend(triggerargs), 0)
    else:
        searchlist = list(commands_list.keys())
        searchitem = triggercommand

    if searchitem.endswith("+"):

        searchitem = searchitem[:-1]
        if not searchitem or not len(searchitem):
            return

        if searchitem.lower() not in searchlist:
            dispmsg = ["Cannot find any alias commands: No valid commands match " + str(searchitem) + "."]
            closestmatches = similar_list(bot, searchitem, searchlist, 10, 'reverse')
            if len(closestmatches):
                dispmsg.append("The following commands match " + str(searchitem) + ": " + spicemanip.main(closestmatches, 'andlist') + ".")
            bot.notice(dispmsg, trigger.nick)
            return

        realcom = searchitem
        if "aliasfor" in commands_list[searchitem].keys():
            realcom = commands_list[searchitem]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.notice("The following commands match " + str(searchitem) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick)
        return

    if searchitem.endswith("?"):

        searchitem = searchitem[:-1]
        if not searchitem or not len(searchitem):
            return

        closestmatches = similar_list(bot, searchitem, searchlist, 10, 'reverse')
        if not len(closestmatches):
            bot.notice("Cannot find any similar commands for " + str(searchitem) + ".", trigger.nick)
        else:
            bot.notice("The following commands may match " + str(searchitem) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick)
        return

    commandlist = []
    for command in searchlist:
        if command.lower().startswith(str(searchitem).lower()):
            commandlist.append(command)

    if not len(commandlist):
        bot.notice("No commands start with " + str(searchitem) + ".", trigger.nick)
    else:
        bot.notice("The following commands start with " + str(searchitem) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
