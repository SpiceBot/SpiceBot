# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


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
        trigger_args, trigger_command = SpiceBot.prerun.trigger_args(message, 'nickname')
        if trigger_command in SpiceBot.commands.dict['commands']["nickname"].keys():
            return

    returnmessage = SpiceBot.botai.on_message(bot, trigger, message)
    if returnmessage:
        bot.osd(str(returnmessage))
