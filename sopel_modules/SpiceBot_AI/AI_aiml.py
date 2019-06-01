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

    if str(trigger.args[1]).startswith((".", '?', '!')) or str(trigger.args[1]).lower().startswith(bot.nick.lower()):
        return

    bot.osd(str(SpiceBot.botai.on_message(str(bot, trigger, trigger.args[1]))))
