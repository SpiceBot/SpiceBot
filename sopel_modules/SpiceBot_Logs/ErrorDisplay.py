# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_Events.System import bot_events_recieved
from sopel_modules.SpiceBot_SBTools import bot_logging
from .Logs import stdio_logs_fetch


@sopel.module.event('2005')
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    debuglines = stdio_logs_fetch(bot)

    searchphrasefound = []
    for line in debuglines:
        if "modules failed to load" in str(line) and "0 modules failed to load" not in str(line):
            searchphrase = str(line).replace(" modules failed to load", "")
            searchphrasefound.append(str(searchphrase) + " module(s) failed")
        elif "dict files failed to load" in str(line) and "0 dict files failed to load" not in str(line):
            searchphrase = str(line).replace(" dict files failed to load", "")
            searchphrasefound.append(str(searchphrase) + " dict file(s) failed")

    if len(searchphrasefound):
        for foundphase in searchphrasefound:
            bot_logging(bot, 'SpiceBot_Logs', str(foundphase))
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        bot.osd(searchphrasefound, bot.channels.keys())
    else:
        bot_logging(bot, 'SpiceBot_Logs', "No issues found at bot startup!")
