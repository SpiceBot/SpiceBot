# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.rule('(.*)')
def bot_command_nick(bot, trigger):

    if trigger.nick == bot.nick:
        return

    if not len(trigger.args):
        return

    message = trigger.args[1]

    # ignore text coming from a valid prefix
    if str(message).startswith(tuple(bot.config.core.prefix_list)):
        return

    returnmessage = SpiceBot.botai.on_message(bot, trigger, message)
    if returnmessage:
        bot.osd(str(returnmessage))
