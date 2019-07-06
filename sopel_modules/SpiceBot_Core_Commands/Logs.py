# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Logs System
"""

# sopel imports
import sopel.module

from sopel_modules.spicemanip import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('logs', 'debug')
def bot_command_logs(bot, trigger, botcom):

    if not SpiceBot.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "I was unable to process this Bot Nick command due to privilege issues.")
        return

    logtype = spicemanip(botcom.dict['args'], 1) or None
    if not logtype:
        bot.osd("Current valid log(s) include: " + spicemanip(list(SpiceBot.logs.dict["list"].keys()), 'andlist'), trigger.sender, 'action')
        return

    if not SpiceBot.inlist(logtype, list(SpiceBot.logs.dict["list"].keys())):
        closestmatches = SpiceBot.similar_list(logtype, list(SpiceBot.logs.dict["list"].keys()), 10, 'reverse')
        if not len(closestmatches):
            SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "No valid logs match " + str(logtype) + ".", trigger.nick, 'notice')
        else:
            SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "The following commands may match " + str(logtype) + ": " + spicemanip(closestmatches, 'andlist') + ".", trigger.nick, 'notice')

        return

    logtype = SpiceBot.inlist_match(logtype, list(SpiceBot.logs.dict["list"].keys()))

    logindex = SpiceBot.logs.get_logs(logtype)

    if not len(logindex):
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "No logs found for " + str(logtype) + ".")
        return

    bot.osd("Is Examining " + str(logtype) + " log(s).")
    for line in logindex:
        bot.osd("    " + str(line))
    bot.osd(str(logtype) + " log(s) Complete.")
