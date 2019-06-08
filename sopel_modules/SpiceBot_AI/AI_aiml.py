# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip


@sopel.module.rule('(.*)')
def bot_command_rule(bot, trigger):

    # TODO add config limits
    # but still allow in privmsg

    if trigger.nick == bot.nick:
        return

    if not len(trigger.args):
        return

    message = trigger.args[1]
    message = ''.join([x for x in message if ord(x) < 128])

    # ignore text coming from a valid prefix
    if str(message).startswith(tuple(bot.config.core.prefix_list)):
        return
        trigger_args, trigger_command = SpiceBot.prerun.trigger_args(message, 'module')
        # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
        if trigger_command.startswith("."):
            return
        commands_list = []
        for commandstype in SpiceBot.commands.dict['commands'].keys():
            if commandstype not in ['rule', 'nickname']:
                for com in SpiceBot.commands.dict['commands'][commandstype].keys():
                    if com not in commands_list:
                        commands_list.append(com)
        if trigger_command not in commands_list:
            if not SpiceBot.letters_in_string(trigger_command):
                return
            invalid_display = ["I don't seem to have a command for " + str(trigger_command) + "!"]
            # invalid_display.append("If you have a suggestion for this command, you can run .feature ." + str(trigger_command))
            # invalid_display.append("ADD DESCRIPTION HERE!")
            bot.osd(invalid_display, trigger.nick, 'notice')
        return

    if str(message).lower().startswith(str(bot.nick).lower()):
        command_type = 'nickname'
        trigger_args, trigger_command = SpiceBot.prerun.trigger_args(message, 'nickname')
        trigger_args.insert(0, trigger_command)
        fulltrigger = spicemanip.main(trigger_args, 0)
        if str(trigger_command).startswith("?"):
            return
        if fulltrigger in SpiceBot.commands.dict['nickrules']:
            return
        if trigger_command in SpiceBot.commands.dict['commands']["nickname"].keys():
            return
    else:
        command_type = 'other'
        trigger_args = spicemanip.main(message, 'create')
        trigger_command = trigger_args[0]
        fulltrigger = spicemanip.main(trigger_args, 0)

    returnmessage = SpiceBot.botai.on_message(bot, trigger, message)
    if returnmessage:
        bot.osd(str(returnmessage))
    else:
        if command_type == 'nickname':

            if trigger_args[0].lower() in ["what", "where"] and trigger_args[1].lower() in ["is", "are"]:
                # TODO saved definitions
                searchterm = spicemanip.main(trigger_args, "3+") or None
                if searchterm:
                    if trigger_args[0].lower() == "where":
                        searchreturn = SpiceBot.googlesearch(searchterm, 'maps')
                    else:
                        searchreturn = SpiceBot.googlesearch(searchterm)
                    if not searchreturn:
                        bot.osd('I cannot find anything about that')
                    else:
                        bot.osd(str(searchreturn))
                return

            elif trigger_args[0].lower() in ["can"] and trigger_args[1].lower() in ["you"] and trigger_args[2].lower() in ["see"]:
                target = spicemanip.main(trigger_args, "4+") or None
                if target:
                    if SpiceBot.inlist(trigger.nick, bot.users):
                        realtarget = SpiceBot.inlist_match(target, bot.users)
                        dispmsg = [trigger.nick + ", yes. I can see " + realtarget]
                        targetchannels = []
                        for channel in bot.channels.keys():
                            if SpiceBot.inlist(trigger.nick, bot.channels[channel].privileges.keys()):
                                targetchannels.append(channel)
                        dispmsg.append(realtarget + " is in " + spicemanip.main(targetchannels, 'andlist'))
                        bot.osd(dispmsg)
                    else:
                        bot.osd(trigger.nick + ", no. I cannot see " + target + " right now!")
                        # if bot_check_inlist(target, bot.memory["botdict"]["users"].keys()):
                        #    bot.osd(trigger.nick + ", I can't see " + inlist_match(target, bot.users) + " at the moment.")
                        # else:
                        #    bot.osd("I have never seen " + str(target) + ".")
                        # user in bot.channels[channel].privileges.keys()
                        # TODO
                return

            closestmatches = SpiceBot.similar_list(trigger_command, SpiceBot.commands.dict['commands']["nickname"].keys(), 3, 'reverse')
            if len(closestmatches):
                closestmatches = spicemanip.main(closestmatches, "andlist")
                bot.osd("I don't know what you are asking me to do! Did you mean: " + str(closestmatches) + "?")
                return
            else:
                bot.osd("I don't know what you are asking me to do!")
                return
