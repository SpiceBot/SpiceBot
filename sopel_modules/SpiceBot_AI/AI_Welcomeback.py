# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip


@sopel.module.rule(r'(?i)(welcome back),? $nickname\?')
def bot_command_really(bot, trigger):
    reply = spicemanip.main(['Thank you', 'thanks'], "random")
    bot.osd(trigger.nick + ", " + reply)
