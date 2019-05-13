# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel
import sopel.module

from difflib import SequenceMatcher
from operator import itemgetter

from sopel_modules.SpiceBot_Events.System import bot_events_check
from sopel_modules.SpiceBot_SBTools import sopel_triggerargs


import spicemanip


@sopel.module.rule('^\?(.*)')
def query_detection(bot, trigger):

    while not bot_events_check(bot, '2002'):
        pass

    commands_list = bot.memory['SpiceBot_CommandsQuery']['commands_all']

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'query_command')

    # command issued, check if valid
    if not triggercommand:
        return
        bot.say("no triggercommand")
    bot.say(str(triggercommand))

    if len(triggercommand) == 1:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(triggercommand):
                commandlist.append(command)
        if commandlist == []:
            bot.notice("No commands match " + str(triggercommand) + ".", trigger.nick)
            return
        else:
            bot.notice("The following commands match " + str(triggercommand) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
            return

    elif triggercommand.endswith("+"):
        triggercommand = triggercommand[:-1]
        if triggercommand not in commands_list.keys():
            bot.notice("The " + str(triggercommand) + " does not appear to be valid.")
            return
        realcom = triggercommand
        if "aliasfor" in commands_list[triggercommand].keys():
            realcom = commands_list[triggercommand]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.notice("The following commands match " + str(triggercommand) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick)
        return

    elif triggercommand.endswith('?'):
        triggercommand = triggercommand[:-1]
        sim_com, sim_num = [], []
        for com in commands_list.keys():
            similarlevel = SequenceMatcher(None, triggercommand.lower(), com.lower()).ratio()
            sim_com.append(com)
            sim_num.append(similarlevel)
        sim_num, sim_com = (list(x) for x in zip(*sorted(zip(sim_num, sim_com), key=itemgetter(0))))
        closestmatch = spicemanip.main(sim_com, 'reverse', "list")
        listnumb, relist = 1, []
        for item in closestmatch:
            if listnumb <= 10:
                relist.append(str(item))
            listnumb += 1
        bot.notice("The following commands may match " + str(triggercommand) + ": " + spicemanip.main(relist, 'andlist') + ".", trigger.nick)
        return

    elif triggercommand in commands_list.keys():
        bot.notice("The following commands match " + str(triggercommand) + ": " + str(triggercommand) + ".", trigger.nick)
        return

    else:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(triggercommand):
                commandlist.append(command)
        if commandlist == []:
            bot.notice("No commands match " + str(triggercommand) + ".", trigger.nick)
            return
        else:
            bot.notice("The following commands match " + str(triggercommand) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
            return
