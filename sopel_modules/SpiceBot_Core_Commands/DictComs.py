# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot DictCom system
"""

import copy

# sopel imports
import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun.prerun('prefix')
@sopel.module.commands('(.*)')
def command_dictcom(bot, trigger):

    if trigger.sb['com'] not in list(SpiceBot.commands.dict['commands']["prefix"].keys()):
        return

    # command aliases
    if "aliasfor" in list(SpiceBot.commands.dict['commands']["prefix"][trigger.sb['com']].keys()):
        trigger.sb['com'] = SpiceBot.commands.dict['commands']["prefix"][trigger.sb['com']]["aliasfor"]

    # simplify usage of the bot command going forward
    # copy dict to not overwrite
    trigger.sb['comdict'] = copy.deepcopy(SpiceBot.commands.dict['commands']["prefix"][trigger.sb['com']])

    # execute function based on command type
    trigger.sb['comtype'] = trigger.sb['comdict']["type"].lower()
