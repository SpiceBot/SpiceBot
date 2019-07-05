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
    totalusers = len(list(SpiceBot.users.dict["all"]))
    onlineusers = len(list(SpiceBot.users.dict["online"]))
    bot.osd("Of the " + str(totalusers) + " users that I've seen, " + str(onlineusers) + " are online currently.")
