# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Users system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('users', 'user')
def nickname_comand_users(bot, trigger, botcom):
    bot.say("WIP")
    return
