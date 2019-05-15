# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_Events.System import bot_events_recieved, botevents
from sopel_modules.SpiceBot_SBTools import bot_logging
from .Logs import stdio_logs_fetch


@sopel.module.event(botevents.BOT_STARTUPMONOLOGUE)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    debuglines = stdio_logs_fetch(bot)

    searchphrasefound = []
    for line in debuglines:
        if str(line).endswith("failed to load") and not str(line).startswith("0"):
            searchphrasefound.append(line)

    if len(searchphrasefound):
        for foundphase in searchphrasefound:
            bot_logging(bot, 'SpiceBot_Logs', str(foundphase))
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        bot.osd(searchphrasefound, bot.channels.keys())
    else:
        bot_logging(bot, 'SpiceBot_Logs', "No issues found at bot startup!", True)