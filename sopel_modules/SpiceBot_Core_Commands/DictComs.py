# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot DictCom system
"""

# sopel imports
import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun.prerun('prefix')
@sopel.module.commands('(.*)')
def command_dictcom(bot, trigger):

    if trigger.sb['com'] not in list(SpiceBot.commands.dict['commands']["prefix"].keys()):
        return

    bot.say("here")
