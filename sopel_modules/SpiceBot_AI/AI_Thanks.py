# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module


@sopel.module.rule(r'(?i)(thank you|thanks),? $nickname[ \t]*$')
def bot_command_thanks(bot, trigger):
    bot.reply("You're welcome.")


@sopel.module.rule('$nickname (thank you)')
def bot_command_thanks_b(bot, trigger):
    bot_command_thanks(bot, trigger)


@sopel.module.nickname_commands('thanks')
def bot_command_thanks_c(bot, trigger):
    bot_command_thanks(bot, trigger)
