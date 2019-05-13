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
    bot.say(str(triggerargs))
    bot.say(str(triggercommand))

    triggerargsarray = spicemanip.main(trigger, 'create')

    # command issued, check if valid
    querycommand = spicemanip.main(triggerargsarray, 1).lower()[1:] or None
    if not querycommand:
        return
        bot.say(str(querycommand))
    bot.say("no querycommand")

    if len(querycommand) == 1:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(querycommand):
                commandlist.append(command)
        if commandlist == []:
            bot.notice("No commands match " + str(querycommand) + ".", trigger.nick)
            return
        else:
            bot.notice("The following commands match " + str(querycommand) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
            return

    elif querycommand.endswith("+"):
        querycommand = querycommand[:-1]
        if querycommand not in commands_list.keys():
            bot.notice("The " + str(querycommand) + " does not appear to be valid.")
            return
        realcom = querycommand
        if "aliasfor" in commands_list[querycommand].keys():
            realcom = commands_list[querycommand]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.notice("The following commands match " + str(querycommand) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick)
        return

    elif querycommand.endswith('?'):
        querycommand = querycommand[:-1]
        sim_com, sim_num = [], []
        for com in commands_list.keys():
            similarlevel = SequenceMatcher(None, querycommand.lower(), com.lower()).ratio()
            sim_com.append(com)
            sim_num.append(similarlevel)
        sim_num, sim_com = (list(x) for x in zip(*sorted(zip(sim_num, sim_com), key=itemgetter(0))))
        closestmatch = spicemanip.main(sim_com, 'reverse', "list")
        listnumb, relist = 1, []
        for item in closestmatch:
            if listnumb <= 10:
                relist.append(str(item))
            listnumb += 1
        bot.notice("The following commands may match " + str(querycommand) + ": " + spicemanip.main(relist, 'andlist') + ".", trigger.nick)
        return

    elif querycommand in commands_list.keys():
        bot.notice("The following commands match " + str(querycommand) + ": " + str(querycommand) + ".", trigger.nick)
        return

    else:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(querycommand):
                commandlist.append(command)
        if commandlist == []:
            bot.notice("No commands match " + str(querycommand) + ".", trigger.nick)
            return
        else:
            bot.notice("The following commands match " + str(querycommand) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
            return
