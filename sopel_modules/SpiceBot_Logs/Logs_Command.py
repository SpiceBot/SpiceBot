# coding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents
from sopel_modules.SpiceBot.Tools import sopel_triggerargs, command_permissions_check, inlist, inlist_match, similar_list


@botevents.check_ready([botevents.BOT_LOGS])
@sopel.module.nickname_commands('logs', 'debug')
def bot_command_logs(bot, trigger):

    if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    logtype = spicemanip.main(triggerargs, 1) or None
    if not logtype:
        bot.osd("Current valid log(s) include: " + spicemanip.main(botlogs.SpiceBot_Logs["list"].keys(), 'andlist'), trigger.sender, 'action')
        return

    if not inlist(logtype, botlogs.SpiceBot_Logs["list"].keys()):
        closestmatches = similar_list(bot, logtype, botlogs.SpiceBot_Logs["list"].keys(), 10, 'reverse')
        if not len(closestmatches):
            bot.notice("No valid logs match " + str(logtype) + ".", trigger.nick)
        else:
            bot.notice("The following commands may match " + str(logtype) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick)

        return

    logtype = inlist_match(logtype, botlogs.SpiceBot_Logs["list"].keys())

    if logtype == "Sopel_systemd":
        logindex = botlogs.systemd_logs_fetch(bot)
    elif logtype == "Sopel_stdio":
        logindex = botlogs.stdio_logs_fetch(bot)
    else:
        logindex = botlogs.SpiceBot_Logs["list"][logtype]

    if not len(logindex):
        bot.osd("No logs found for " + str(logtype) + ".")
        return

    bot.osd("Is Examining " + str(logtype) + " log(s).")
    for line in logindex:
        bot.osd("    " + str(line))
    bot.osd(str(logtype) + " log(s) Complete.")
