# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot regnicks system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot
from sopel_modules.spicemanip import spicemanip


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('regnicks', 'regnick')
def nickname_comand_regnicks(bot, trigger, botcom):
    reggedusers = SpiceBot.users.dict["registered"]
    bot.osd("These users are registered " + spicemanip(reggedusers, 'andlist') + ".", trigger.sender, 'notice')
    notregged = []
    for user in SpiceBot.users.dict["online"]:
        usernick = SpiceBot.users.ID(user)
        if str(usernick).lower() in [x.lower() for x in SpiceBot.users.dict["registered"]]:
            notregged.append(usernick)
    bot.osd("These online users are not registered " + spicemanip(notregged, 'andlist') + ".", trigger.sender, 'notice')
