# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module


@sopel.module.nickname_commands('gender')
def bot_command_gender(bot, trigger):
    bot.osd("If societal genders are binary, my gender is female")
