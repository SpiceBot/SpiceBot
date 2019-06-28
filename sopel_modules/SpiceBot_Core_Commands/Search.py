# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot search system.
"""
import sopel

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('module')
@sopel.module.commands('search', 'find', 'google', 'lookup')
def search_main(bot, trigger, botcom):

    searchterm = spicemanip.main(trigger.sb['args'], 0) or None
    if not searchterm:
        bot.osd("Not sure what you want me to look for.")
        return

    searchreturn = SpiceBot.google.search(searchterm)
    if not searchreturn:
        bot.osd('I cannot find anything about that')
    else:
        bot.osd(["[Information search for '" + str(searchterm) + "']", str(searchreturn)])


@SpiceBot.prerun('module')
@sopel.module.commands("where", "whereis")
def search_where(bot, trigger, botcom):

    searchterm = spicemanip.main(trigger.sb['args'], 0) or None
    if not searchterm:
        bot.osd("Not sure what you want me to look for.")
        return

    searchreturn = SpiceBot.google.search(searchterm, 'maps')
    if not searchreturn:
        bot.osd('I cannot find anything about that')
    else:
        bot.osd(["[Location search for " + str(searchterm) + "]", str(searchreturn)])


@SpiceBot.prerun('module')
@sopel.module.commands("what", "whatis")
def search_what(bot, trigger, botcom):

    searchterm = spicemanip.main(trigger.sb['args'], 0) or None
    if not searchterm:
        bot.osd("Not sure what you want me to look for.")
        return

    searchreturn = SpiceBot.google.search(searchterm)
    if not searchreturn:
        bot.osd('I cannot find anything about that')
    else:
        bot.osd(["[Information search for '" + str(searchterm) + "']", str(searchreturn)])


@SpiceBot.prerun('module')
@sopel.module.commands("youtube", "video")
def search_video(bot, trigger, botcom):

    searchterm = spicemanip.main(trigger.sb['args'], 0) or None
    if not searchterm:
        bot.osd("Not sure what you want me to look for.")
        return

    searchreturn = SpiceBot.google.search(searchterm, 'youtube')
    if not searchreturn:
        bot.osd('I cannot find anything about that')
    else:
        bot.osd(["[Youtube search for '" + str(searchterm) + "']", str(searchreturn)])
