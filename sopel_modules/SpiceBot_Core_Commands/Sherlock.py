# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function

# sopel imports
import sopel.module

from sopel_modules.spicemanip import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('module')
@sopel.module.commands('sherlock', 'username')
def bot_command_sherlock(bot, trigger, botcom):

    netlist = list(SpiceBot.sherlock.dict.keys())

    username = spicemanip(botcom.dict["args"], 1) or trigger.nick
    botcom.dict["args"] = spicemanip(botcom.dict["args"], "2+", 'list')

    checklist = netlist
    checklistname = 'all'
    if SpiceBot.inlist(username, netlist):
        checklistname = SpiceBot.inlist_match(username, netlist)
        checklist = [checklistname]
        username = spicemanip(botcom.dict["args"], 1) or trigger.nick

    bot.osd("Checking username " + username + " in " + checklistname + " network.")

    inlist, notinlist = [], []

    for social_network in checklist:

        in_social = SpiceBot.sherlock.check_network(username, social_network)
        if in_social:
            inlist.append(social_network)
        else:
            notinlist.append(social_network)

    if len(inlist):
        if checklistname != 'all':
            bot.osd(["The username " + username + " is in " + checklist[0], SpiceBot.sherlock.dict.get(social_network).get("url").format(username)])
        else:
            bot.osd(["The username " + username + " is in the following:", spicemanip(inlist, "andlist")], trigger.nick, 'NOTICE')
    if len(notinlist):
        if checklistname != 'all':
            bot.osd(["The username " + username + " is NOT in the following:", spicemanip(notinlist, "andlist")])
        else:
            bot.osd(["The username " + username + " is NOT in the following:", spicemanip(notinlist, "andlist")], trigger.nick, 'NOTICE')
