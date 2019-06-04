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

    # ignore text coming from a valid prefix
    if str(message).startswith(tuple(bot.config.core.prefix_list)):
        return

    if str(message).lower().startswith(str(bot.nick).lower()):
        command_type = 'nickname'
        trigger_args, trigger_command = SpiceBot.prerun.trigger_args(message, 'nickname')
        if str(trigger_command).startswith("?"):
            return
        fulltrigger = spicemanip.main(trigger_args, 0)
        if fulltrigger in SpiceBot.commands.dict['nickrules']:
            return
        if trigger_command in SpiceBot.commands.dict['commands']["nickname"].keys():
            return
    else:
        command_type = 'module'
        trigger_args, trigger_command = SpiceBot.prerun.trigger_args(message, 'module')

    returnmessage = SpiceBot.botai.on_message(bot, trigger, message)
    if returnmessage:
        bot.osd(str(returnmessage))
    else:
        if command_type == 'nickname':
            closestmatches = SpiceBot.similar_list(trigger_command, SpiceBot.commands.dict['commands']["nickname"].keys(), 3, 'reverse')
            if len(closestmatches):
                closestmatches = spicemanip.main(closestmatches, "andlist")
                bot.osd("I don't know what you are asking me to do! Did you mean: " + str(closestmatches) + "?")
                return
            else:
                bot.osd("I don't know what you are asking me to do!")
                return
