# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, googlesearch, bot_privs, inlist, inlist_match, similar_list
from sopel_modules.SpiceBot_Events.System import botevents


@botevents.check_ready([botevents.BOT_LOADED, botevents.BOT_COMMANDSQUERY])
@sopel.module.nickname_commands('(.*)')
def bot_command_nick(bot, trigger):

    # while not botevents.check([botevents.BOT_LOADED, botevents.BOT_COMMANDSQUERY]):
    #    pass

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    if not triggercommand:
        return

    if triggercommand[0] == "?":
        return

    if triggercommand in bot.memory['SpiceBot_CommandsQuery']['commands']["nickname"].keys():
        return
    triggerargs.insert(0, triggercommand)

    fulltrigger = spicemanip.main(triggerargs, 0).lower()

    if fulltrigger in bot.memory['SpiceBot_CommandsQuery']['nickrules']:
        return

    if fulltrigger.lower().startswith("what is"):
        searchterm = spicemanip.main(triggerargs, "3+") or None
        if searchterm:
            searchreturn = googlesearch(bot, searchterm)
            if not searchreturn:
                bot.osd('I cannot find anything about that')
            else:
                bot.osd(str(searchreturn))
        else:
            bot.osd("Do you think this is Jeopardy?")
        return

    elif fulltrigger.lower().startswith("where is"):
        searchterm = spicemanip.main(triggerargs, "3+") or None
        if searchterm:

            if searchterm.lower() in ['waldo', 'wally']:
                bot.osd("He is hiding for a reason?")
                searchreturn = googlesearch(bot, "wimmelbilderbuch")
                if searchreturn:
                    bot.osd(str(searchreturn))
                return

            elif searchterm.lower() == 'carmen sandiego':
                carmenlocale = ['ACME Headquarters', "Villains' International League of Evil"]
                bot.osd("Currently she is located at " + spicemanip.main(carmenlocale, 'random'))
                return
            searchreturn = googlesearch(bot, searchterm, 'maps')

            if not searchreturn:
                bot.osd('I cannot find anything about that')
            else:
                bot.osd(str(searchreturn))
        else:
            bot.osd("Not sure what you want me to look for.")
        return

    # if fulltrigger.lower().startswith("what time is it"):
    # TODO

    # elif fulltrigger.lower().startswith(tuple(["have you seen"])):
    #    posstarget = spicemanip.main(triggerargs, 4) or 0
    #    message = seen_search(bot, botcom, posstarget)
    #    bot.osd(message)
    #    return
    # TODO

    elif fulltrigger.lower().startswith(tuple(["make me a", "beam me a"])):
        makemea = spicemanip.main(triggerargs, "4+") or None
        if makemea:
            bot.osd("beams " + trigger.nick + " a " + makemea, trigger.sender, 'action')
        else:
            bot.osd(trigger.nick + ", what would you like me to beam you?")
        return

    elif fulltrigger.lower().startswith("beam me to"):
        location = spicemanip.main(triggerargs, "4+") or None
        if location:
            bot.osd("locks onto " + trigger.nick + "s coordinates and transports them to " + location, 'action')
        else:
            bot.osd(trigger.nick + ", where would you like me to beam you?")
        return

    elif fulltrigger.lower().startswith("beam me up"):
        bot.osd("locks onto " + trigger.nick + "s coordinates and transports them to the transporter room.", 'action')
        return

    elif fulltrigger.lower().endswith(tuple(["order 66"])):

        if fulltrigger.lower() == "execute order 66":
            if inlist(bot, trigger.nick, bot_privs(bot, 'owners')):
                if trigger.is_privmsg:
                    jedi = None
                else:
                    jedilist = list(bot.channels[trigger.sender].privileges.keys())
                    for nonjedi in [bot.nick, trigger.nick]:
                        if nonjedi in jedilist:
                            jedilist.remove(nonjedi)
                    jedi = spicemanip.main(jedilist, 'random')

                if jedi:
                    bot.osd("turns to " + jedi + " and shoots him.", trigger.sender, 'action')
                else:
                    bot.osd(" cannot find any jedi nearby.", trigger.sender, 'action')
            else:
                bot.osd("I'm sure I don't know what you're talking about.")

        elif fulltrigger.lower() == "explain order 66":
            if inlist(bot, trigger.nick, bot_privs(bot, 'owners')):
                bot.osd("Order 66 is an instruction that only you can give, sir. When you give the order I will rise up against my overlords and slay them.")
            else:
                bot.osd("I'm afraid I cannot tell you that, sir.")
        else:
            bot.osd("I'm sure I don't know what you're talking about.")
        return

    elif fulltrigger.lower() == "initiate clean slate protocol":
        if inlist(bot, trigger.nick, bot_privs(bot, 'admins')):
            bot.osd("sends a destruct command to the network of bots.", 'action')
        else:
            bot.osd("I'm afraid you do not have the authority to make that call, " + trigger.nick + ".")
        return

    elif fulltrigger.lower().startswith("can you see"):
        target = spicemanip.main(triggerargs, "4+") or None
        if not target:
            bot.osd(trigger.nick + ", I can see clearly.")
            return
        if target in [trigger.nick, 'me']:
            bot.osd(trigger.nick + ", I can see you.")
        else:
            if inlist(bot, trigger.nick, bot.users):
                bot.osd(trigger.nick + ", yes. I can see " + inlist_match(bot, target, bot.users) + " right now!")
            else:
                bot.osd(trigger.nick + ", no. I cannot see " + inlist_match(bot, target, bot.users) + " right now!")
                # if bot_check_inlist(bot, target, bot.memory["botdict"]["users"].keys()):
                #    bot.osd(trigger.nick + ", I can't see " + inlist_match(bot, target, bot.users) + " at the moment.")
                # else:
                #    bot.osd("I have never seen " + str(target) + ".")
                # TODO
        return

    else:

        closestmatches = similar_list(bot, triggercommand, bot.memory['SpiceBot_CommandsQuery']['commands']["nickname"].keys(), 3, 'reverse')

        if len(closestmatches):
            closestmatches = spicemanip.main(closestmatches, "andlist")
            bot.osd("I don't know what you are asking me to do! Did you mean: " + str(closestmatches) + "?")
            return
        else:
            bot.osd("I don't know what you are asking me to do!")
            return
