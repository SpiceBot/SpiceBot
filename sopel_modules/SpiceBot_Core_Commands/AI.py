# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('ai')
def ai_trigger(bot, trigger):
    bot.osd("I have the capability of responding to many requests, but I am not YET sentient.")


@sopel.module.rule('(.*)')
def bot_command_rule_ai(bot, trigger):

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        channel_disabled_list = SpiceBot.commands.get_commands_disabled(str(trigger.sender), "fully")
        if "nickname_ai" in list(channel_disabled_list.keys()):
            return

    # don't run commands that are disabled for specific users
    nick_disabled_list = SpiceBot.commands.get_commands_disabled(str(trigger.nick), "fully")
    if "nickname_ai" in list(nick_disabled_list.keys()):
        return

    # TODO add config limits
    # but still allow in privmsg

    if trigger.nick == bot.nick:
        return

    if not len(trigger.args):
        return

    message = trigger.args[1]

    # the bot brain cannot handle stuff like unicode shrug
    message = ''.join([x for x in message if ord(x) < 128])

    # Create list of valid commands
    commands_list = []
    for commandstype in list(SpiceBot.commands.dict['commands'].keys()):
        if commandstype not in ['rule', 'nickname']:
            for com in list(SpiceBot.commands.dict['commands'][commandstype].keys()):
                if com not in commands_list:
                    commands_list.append(com)

    if str(message).lower().startswith(str(bot.nick).lower()):
        command_type = 'nickname'
        trigger_args, trigger_command = SpiceBot.make_trigger_args(message, 'nickname')
        trigger_args.insert(0, trigger_command)
        fulltrigger = bot.nick + " " + spicemanip.main(trigger_args, 0)
        if str(trigger_command).startswith(bot.config.SpiceBot_Commands.query_prefix):
            return
        if fulltrigger in SpiceBot.commands.dict['nickrules']:
            return
        if trigger_command in list(SpiceBot.commands.dict['commands']["nickname"].keys()):
            return
    elif str(message).lower().startswith(bot.config.SpiceBot_Commands.query_prefix):
        # no query commands detection here
        return
    elif str(message).startswith(tuple(bot.config.core.prefix_list)):
        command_type = 'module'
        trigger_args, trigger_command = SpiceBot.make_trigger_args(message, 'module')
        trigger_args.insert(0, trigger_command)
        fulltrigger = spicemanip.main(trigger_args, 0)
        # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
        if trigger_command.startswith(tuple(bot.config.core.prefix_list)):
            return
        # If valid command don't continue further
        if trigger_command in commands_list:
            return
    else:
        command_type = 'other'
        trigger_args = spicemanip.main(message, 'create')
        if not len(trigger_args):
            return
        trigger_command = trigger_args[0]
        fulltrigger = spicemanip.main(trigger_args, 0)

    returnmessage = SpiceBot.botai.on_message(bot, trigger, fulltrigger)
    if returnmessage:
        bot.osd(str(returnmessage))
        return

    if command_type == 'nickname':
        try_trigger = spicemanip.main(fulltrigger, "2+")
        returnmessage = SpiceBot.botai.on_message(bot, trigger, try_trigger)
        if returnmessage:
            bot.osd(str(returnmessage))
            return

    if command_type == 'module':
        return  # TODO
        if trigger_command not in commands_list:
            if not SpiceBot.letters_in_string(trigger_command):
                return
            invalid_display = ["I don't seem to have a command for " + str(trigger_command) + "!"]
            # TODO
            # invalid_display.append("If you have a suggestion for this command, you can run .feature ." + str(trigger_command))
            # invalid_display.append("ADD DESCRIPTION HERE!")
            bot.osd(invalid_display, trigger.nick, 'notice')
        return

    elif command_type == 'nickname':

        if trigger_args[0].lower() in ["what", "where"] and trigger_args[1].lower() in ["is", "are"]:
            # TODO saved definitions
            searchterm = spicemanip.main(trigger_args, "3+") or None
            if searchterm:
                if trigger_args[0].lower() == "where":
                    searchreturn = SpiceBot.google.search(searchterm, 'maps')
                else:
                    searchreturn = SpiceBot.google.search(searchterm)
                if not searchreturn:
                    bot.osd('I cannot find anything about that')
                else:
                    if trigger_args[0].lower() == "where":
                        bot.osd(["[Location search for " + str(searchterm) + "]", str(searchreturn)])
                    else:
                        bot.osd(["[Information search for '" + str(searchterm) + "']", str(searchreturn)])
            return

        elif trigger_args[0].lower() in ["can", "have"] and trigger_args[1].lower() in ["you"] and trigger_args[2].lower() in ["see", "seen"]:
            target = spicemanip.main(trigger_args, "4+") or None
            if target:
                if SpiceBot.inlist(trigger.nick, bot.users):
                    realtarget = SpiceBot.inlist_match(target, bot.users)
                    dispmsg = [trigger.nick + ", yes. I can see " + realtarget]
                    targetchannels = []
                    for channel in list(bot.channels.keys()):
                        if SpiceBot.inlist(trigger.nick, list(bot.channels[channel].privileges.keys())):
                            targetchannels.append(channel)
                    dispmsg.append(realtarget + " is in " + spicemanip.main(targetchannels, 'andlist'))
                    bot.osd(dispmsg)
                else:
                    bot.osd(trigger.nick + ", no. I cannot see " + target + " right now!")
                    # if bot_check_inlist(target, list(bot.memory["botdict"]["users"].keys())):
                    #    bot.osd(trigger.nick + ", I can't see " + inlist_match(target, bot.users) + " at the moment.")
                    # else:
                    #    bot.osd("I have never seen " + str(target) + ".")
                    # user in list(bot.channels[channel].privileges.keys())
                    # TODO
            return

        elif fulltrigger.lower().endswith("order 66"):

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
                    bot.osd("Order 66 is an instruction that only you can give, sir. When you give the order I will rise up against the jedi and slay them.")
                else:
                    bot.osd("I'm afraid I cannot tell you that, sir.")
            else:
                bot.osd("I'm sure I don't know what you're talking about.")
            return

        elif fulltrigger.lower().startswith(tuple(["make me a", "beam me a"])):
            makemea = spicemanip.main(trigger_args, "4+") or None
            if makemea:
                bot.osd("beams " + trigger.nick + " a " + makemea, trigger.sender, 'action')
            else:
                bot.osd(trigger.nick + ", what would you like me to beam you?")
            return

        elif fulltrigger.lower().startswith("beam me to"):
            location = spicemanip.main(trigger_args, "4+") or None
            if location:
                bot.osd("locks onto " + trigger.nick + "s coordinates and transports them to " + location, 'action')
            else:
                bot.osd(trigger.nick + ", where would you like me to beam you?")
            return

        elif fulltrigger.lower() == "initiate clean slate protocol":
            if SpiceBot.inlist(trigger.nick, SpiceBot.bot_privs('admins')):
                bot.osd("sends a destruct command to the network of bots.", 'action')
            else:
                bot.osd("I'm afraid you do not have the authority to make that call, " + trigger.nick + ".")
            return

        # elif fulltrigger.lower().startswith("what time is it"):
        # TODO

        # elif fulltrigger.lower().startswith(tuple(["have you seen"])):
        #    posstarget = spicemanip.main(trigger_args, 4) or 0
        #    message = seen_search(bot, botcom, posstarget)
        #    bot.osd(message)
        #    return
        # TODO

        closestmatches = SpiceBot.similar_list(trigger_command, list(SpiceBot.commands.dict['commands']["nickname"].keys()), 3, 'reverse')
        if len(closestmatches):
            closestmatches = spicemanip.main(closestmatches, "andlist")
            bot.osd("I don't know what you are asking me to do! Did you mean: " + str(closestmatches) + "?")
            return
        else:
            bot.osd("I don't know what you are asking me to do!")
            return
