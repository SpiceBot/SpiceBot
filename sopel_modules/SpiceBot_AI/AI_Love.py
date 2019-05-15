# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module


@sopel.module.rule(r'(?i)(I love you|loveya),? $nickname[ \t]*$')
def bot_command_love(bot, trigger):
    bot.reply("I love you too.")


@sopel.module.rule('$nickname (loveya|I love you)')
def bot_command_love_b(bot, trigger):
    bot_command_love(bot, trigger)


@sopel.module.nickname_commands('loveya')
def bot_command_love_c(bot, trigger):
    bot_command_love(bot, trigger)


@sopel.module.rule('(I love) $nickname')
def bot_command_love_d(bot, trigger):
    bot_command_like(bot, trigger)


@sopel.module.rule(r'(?i)(I like you),? $nickname[ \t]*$')
def bot_command_like(bot, trigger):
    bot.reply("I like you too.")


@sopel.module.rule('$nickname (I like you)')
def bot_command_like_b(bot, trigger):
    bot_command_like(bot, trigger)


@sopel.module.rule('(I like) $nickname')
def bot_command_like_c(bot, trigger):
    bot_command_like(bot, trigger)
