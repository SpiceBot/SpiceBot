# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, command_permissions_check, inlist, inlist_match
from sopel_modules.SpiceBot_Events.System import bot_events_check
from .Logs import systemd_logs_fetch, stdio_logs_fetch


@sopel.module.nickname_commands('logs', 'debug')
def bot_command_logs(bot, trigger):

    while not bot_events_check(bot, '2004'):
        pass

    if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    logtype = spicemanip.main(triggerargs, 1) or None
    if not logtype or not inlist(bot, logtype, bot.memory['SpiceBot_Logs']["logs"].keys()):
        bot.osd("Current valid log(s) include: " + spicemanip.main(bot.memory['SpiceBot_Logs']["logs"].keys(), 'andlist'), trigger.sender, 'action')
        return

    logtype = inlist_match(bot, logtype, bot.memory['SpiceBot_Logs']["logs"].keys())

    if logtype == "Sopel_systemd":
        logindex = systemd_logs_fetch(bot)
    elif logtype == "Sopel_stdio":
        logindex = stdio_logs_fetch(bot)
    else:
        logindex = bot.memory['SpiceBot_Logs']["logs"][logtype]

    if not len(logindex):
        bot.osd("No logs found for " + str(logtype) + ".")
        return

    bot.osd("Is Examining " + str(logtype) + " log(s).")
    for line in logindex:
        bot.osd("    " + str(line))
    bot.osd(str(logtype) + " log(s) Complete.")
