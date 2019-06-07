# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOADED, SpiceBot.events.BOT_COMMANDS])
@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('(.*)')
def bot_command_nick(bot, trigger):

    if not trigger.sb['com']:
        return

    if trigger.sb['com'][0] == "?":
        return

    if trigger.sb['com'] in SpiceBot.commands.dict['commands']["nickname"].keys():
        return
    trigger.sb['args'].insert(0, trigger.sb['com'])

    fulltrigger = spicemanip.main(trigger.sb['args'], 0).lower()

    # if fulltrigger.lower().startswith("what time is it"):
    # TODO

    # elif fulltrigger.lower().startswith(tuple(["have you seen"])):
    #    posstarget = spicemanip.main(trigger.sb['args'], 4) or 0
    #    message = seen_search(bot, botcom, posstarget)
    #    bot.osd(message)
    #    return
    # TODO

    if fulltrigger.lower().startswith(tuple(["make me a", "beam me a"])):
        makemea = spicemanip.main(trigger.sb['args'], "4+") or None
        if makemea:
            bot.osd("beams " + trigger.nick + " a " + makemea, trigger.sender, 'action')
        else:
            bot.osd(trigger.nick + ", what would you like me to beam you?")
        return

    elif fulltrigger.lower().startswith("beam me to"):
        location = spicemanip.main(trigger.sb['args'], "4+") or None
        if location:
            bot.osd("locks onto " + trigger.nick + "s coordinates and transports them to " + location, 'action')
        else:
            bot.osd(trigger.nick + ", where would you like me to beam you?")
        return

    elif fulltrigger.lower().endswith(tuple(["order 66"])):

        if fulltrigger.lower() == "execute order 66":
            if SpiceBot.inlist(trigger.nick, SpiceBot.bot_privs('owners')):
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
            if SpiceBot.inlist(trigger.nick, SpiceBot.bot_privs('owners')):
                bot.osd("Order 66 is an instruction that only you can give, sir. When you give the order I will rise up against my overlords and slay them.")
            else:
                bot.osd("I'm afraid I cannot tell you that, sir.")
        else:
            bot.osd("I'm sure I don't know what you're talking about.")
        return

    elif fulltrigger.lower() == "initiate clean slate protocol":
        if SpiceBot.inlist(trigger.nick, SpiceBot.bot_privs('admins')):
            bot.osd("sends a destruct command to the network of bots.", 'action')
        else:
            bot.osd("I'm afraid you do not have the authority to make that call, " + trigger.nick + ".")
        return
