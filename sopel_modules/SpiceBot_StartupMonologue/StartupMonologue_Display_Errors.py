# coding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_STARTUPMONOLOGUE)
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):

    debuglines = SpiceBot.logs.stdio_logs_fetch(bot)

    searchphrasefound = []
    for line in debuglines:
        if str(line).endswith("failed to load") and not str(line).startswith("0"):
            searchphrasefound.append(line)

    if len(searchphrasefound):
        for foundphase in searchphrasefound:
            SpiceBot.logs.log('SpiceBot_Logs', str(foundphase))
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        bot.osd(searchphrasefound, bot.channels.keys())
    else:
        SpiceBot.logs.log('SpiceBot_Logs', "No issues found at bot startup!", True)
