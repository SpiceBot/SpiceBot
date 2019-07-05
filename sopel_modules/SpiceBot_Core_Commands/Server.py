# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Users system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('server')
def nickname_comand_server(bot, trigger, botcom):
    network = SpiceBot.server.isupport["NETWORK"]
    server = SpiceBot.server.myinfo["servername"]
    version = SpiceBot.server.myinfo["version"]
    bot.osd("I am connected to " + str(server) + " on the " + str(network) + " network. This server runs " + str(version))
