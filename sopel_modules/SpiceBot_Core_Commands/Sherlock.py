# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function

# sopel imports
import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun.prerun('module')
@sopel.module.commands('sherlock', 'username')
def bot_command_sherlock(bot, trigger):

    data = SpiceBot.sherlock.dict
    netlist = list(SpiceBot.sherlock.dict.keys())

    username = spicemanip.main(trigger.sb["args"], 1) or trigger.nick
    trigger.sb["args"] = spicemanip.main(trigger.sb["args"], "2+", 'list')

    checklist = netlist
    checklistname = 'all'
    if SpiceBot.bot_check_inlist(bot, username, netlist):
        checklistname = SpiceBot.inlist_match(bot, username, netlist)
        checklist = [checklistname]
        username = spicemanip.main(trigger.sb["args"], 1) or trigger.nick

    bot.osd("Checking username " + username + " in " + checklistname + " network.")

    inlist = []
    notinlist = []

    for social_network in checklist:

        url = data.get(social_network).get("url").format(username)
        error_type = data.get(social_network).get("errorType")
        cant_have_period = data.get(social_network).get("noPeriod")

        if ("." in username) and (cant_have_period == "True"):
            while ("." in username):
                username = username.replace(".", '')

        r, error_type = SpiceBot.sherlock.make_request(url=url, error_type=error_type, social_network=social_network)

        if error_type == "message":
            error = data.get(social_network).get("errorMsg")
            # Checks if the error message is in the HTML
            if error not in r.text:
                inlist.append(social_network)
            else:
                notinlist.append(social_network)

        elif error_type == "status_code":
            # Checks if the status code of the repsonse is 404
            if not r.status_code == 404:
                inlist.append(social_network)
            else:
                notinlist.append(social_network)

        elif error_type == "response_url":
            error = data.get(social_network).get("errorUrl")
            # Checks if the redirect url is the same as the one defined in data.json
            if error not in r.url:
                inlist.append(social_network)
            else:
                notinlist.append(social_network)

    if inlist != []:
        if checklistname != 'all':
            bot.osd(["The username " + username + " is in " + checklist[0]])
        else:
            bot.osd(["The username " + username + " is in the following:", spicemanip.main(inlist, "andlist")])
    if notinlist != []:
        bot.osd(["The username " + username + " is NOT in the following:", spicemanip.main(notinlist, "andlist")])
