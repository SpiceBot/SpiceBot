# coding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOGS])
@sopel.module.nickname_commands('logs', 'debug')
def bot_command_logs(bot, trigger):

    if not SpiceBot.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = SpiceBot.sopel_triggerargs(bot, trigger, 'nickname_command')

    logtype = spicemanip.main(triggerargs, 1) or None
    if not logtype:
        bot.osd("Current valid log(s) include: " + spicemanip.main(SpiceBot.logs.dict["list"].keys(), 'andlist'), trigger.sender, 'action')
        return

    if not SpiceBot.inlist(logtype, SpiceBot.logs.dict["list"].keys()):
        closestmatches = SpiceBot.similar_list(bot, logtype, SpiceBot.logs.dict["list"].keys(), 10, 'reverse')
        if not len(closestmatches):
            bot.notice("No valid logs match " + str(logtype) + ".", trigger.nick)
        else:
            bot.notice("The following commands may match " + str(logtype) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick)

        return

    logtype = SpiceBot.inlist_match(logtype, SpiceBot.logs.dict["list"].keys())

    logindex = SpiceBot.logs.get_logs(bot, logtype)

    if not len(logindex):
        bot.osd("No logs found for " + str(logtype) + ".")
        return

    bot.osd("Is Examining " + str(logtype) + " log(s).")
    for line in logindex:
        bot.osd("    " + str(line))
    bot.osd(str(logtype) + " log(s) Complete.")
