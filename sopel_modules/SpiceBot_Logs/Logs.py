# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.tools import stderr

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, command_permissions_check, inlist, inlist_match


def configure(config):
    pass


def setup(bot):
    stderr("[SpiceBot_Logs] Starting Setup Procedure")
    bot.memory['SpiceBot_Logs'] = {}


@sopel.module.nickname_commands('logs')
def bot_command_action(bot, trigger):

    if not command_permissions_check(bot, trigger, ['admins', 'owner']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    logtype = spicemanip.main(triggerargs, 1) or None
    if not logtype or not inlist(bot, logtype, bot.memory['SpiceBot_Logs'].keys()):
        bot.osd("Current valid log(s) include: " + spicemanip.main(bot.memory['SpiceBot_Logs'].keys(), 'andlist'), trigger.sender, 'action')
        return

    logtype = inlist_match(bot, logtype, bot.memory['SpiceBot_Logs'].keys())

    if len(bot.memory['SpiceBot_Logs'][logtype]) == 0:
        bot.osd("No logs found for " + str(logtype) + ".")
        return

    bot.osd("Is Examining " + str(logtype) + " log(s).")
    for line in bot.memory['SpiceBot_Logs'][logtype]:
        bot.osd(str(line), trigger.sender, 'action')


def bot_logging(bot, logtype, logentry):

    if 'SpiceBot_Logs' not in bot.memory:
        bot.memory['SpiceBot_Logs'] = {}

    if logtype not in bot.memory['SpiceBot_Logs'].keys():
        bot.memory['SpiceBot_Logs'][logtype] = []

    bot.memory['SpiceBot_Logs'][logtype].append(logentry)
    if len(bot.memory['SpiceBot_Logs'][logtype]) > 10:
        del bot.memory['SpiceBot_Logs'][logtype][0]
