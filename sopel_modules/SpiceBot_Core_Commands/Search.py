# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot search system.
"""
import sopel

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun.prerun('module')
@sopel.module.commands('search', 'find', 'google', 'lookup')
def nickname_comand_commands(bot, trigger):

    searchterm = spicemanip.main(trigger.sb['args'], 0) or None
    if not searchterm:
        bot.osd("Not sure what you want me to look for.")
        return

    searchreturn = SpiceBot.google.search(searchterm)
    if not searchreturn:
        bot.osd('I cannot find anything about that')
    else:
        bot.osd(["[Information search for '" + str(searchterm) + "']", str(searchreturn)])
