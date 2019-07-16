# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Users system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('version')
def nickname_comand_version(bot, trigger, botcom):
    fulldisp = []

    # sopel
    displayval = "I am running Sopel " + str(SpiceBot.version.sopel["version_local_num"])
    if SpiceBot.version.sopel["version_local"] < SpiceBot.version.sopel["version_online"]:
        displayval += " Update Available to " + SpiceBot.version.sopel["version_online_num"]
    fulldisp.append(displayval)

    # SpiceBot
    fulldisp.append("I am running Sopel " + str(SpiceBot.version.spicebot["version_local_num"]))

    bot.osd(fulldisp)
