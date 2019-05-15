# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip


@sopel.module.rule(r'(?i)(bye|goodbye|gtg|seeya|cya|ttyl|g2g|gnight|goodnight),? $nickname[ \t]*$')
def bot_command_goodbye(bot, trigger):
    byemsg = spicemanip.main(['Bye', 'Goodbye', 'Seeya', 'Auf Wiedersehen', 'Au revoir', 'Ttyl'], "random")
    punctuation = spicemanip.main(['!', ''], "random")
    bot.say(byemsg + ' ' + trigger.nick + punctuation)


@sopel.module.nickname_commands("bye", "goodbye", "gtg", "seeya", "cya", "ttyl", "g2g", "gnight", "goodnight")
def bot_command_goodbye_b(bot, trigger):
    bot_command_goodbye(bot, trigger)
