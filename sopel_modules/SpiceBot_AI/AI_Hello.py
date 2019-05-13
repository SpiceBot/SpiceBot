# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip


@sopel.module.rule(r'(?i)(hi|hello|hey),? $nickname[ \t]*$')
def bot_command_hello(bot, trigger):
    hello = spicemanip.main(['Hi', 'Hey', 'Hello'], "random")
    punctuation = spicemanip.main(['', '!', '?'], "random")
    bot.osd(hello + ' ' + trigger.nick + punctuation)


@sopel.module.nickname_commands('hello', 'hi', 'hey')
def bot_command_hello_b(bot, trigger):
    bot_command_hello(bot, trigger)
