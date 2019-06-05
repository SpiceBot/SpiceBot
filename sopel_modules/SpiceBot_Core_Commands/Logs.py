# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Logs System
"""

# sopel imports
import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOGS])
@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('logs', 'debug')
def bot_command_logs(bot, trigger):

    if not SpiceBot.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.osd("I was unable to process this Bot Nick command due to privilege issues.")
        return

    logtype = spicemanip.main(trigger.sb['args'], 1) or None
    if not logtype:
        bot.osd("Current valid log(s) include: " + spicemanip.main(SpiceBot.logs.dict["list"].keys(), 'andlist'), trigger.sender, 'action')
        return

    if not SpiceBot.inlist(logtype, SpiceBot.logs.dict["list"].keys()):
        closestmatches = SpiceBot.similar_list(logtype, SpiceBot.logs.dict["list"].keys(), 10, 'reverse')
        if not len(closestmatches):
            bot.osd("No valid logs match " + str(logtype) + ".", trigger.nick, 'notice')
        else:
            bot.osd("The following commands may match " + str(logtype) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick, 'notice')

        return

    logtype = SpiceBot.inlist_match(logtype, SpiceBot.logs.dict["list"].keys())

    logindex = SpiceBot.logs.get_logs(logtype)

    if not len(logindex):
        bot.osd("No logs found for " + str(logtype) + ".")
        return

    bot.osd("Is Examining " + str(logtype) + " log(s).")
    for line in logindex:
        bot.osd("    " + str(line))
    bot.osd(str(logtype) + " log(s) Complete.")
