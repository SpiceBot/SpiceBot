# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.tools import stderr
from sopel.config.types import StaticSection, ValidatedAttribute

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, command_permissions_check, inlist, inlist_match


def configure(config):
    config.define_section("SpiceBot_Logs", SpiceBot_Logs_MainSection, validate=False)
    config.SpiceBot_Logs.configure_setting('logging_channel', 'SpiceBot_Logs channels')


class SpiceBot_Logs_MainSection(StaticSection):
    logging_channel = ValidatedAttribute('logging_channel', default=False)


def setup(bot):
    bot_logging(bot, 'SpiceBot_Logs', "Starting Setup Procedure")
    bot.config.define_section("SpiceBot_Logs", SpiceBot_Logs_MainSection, validate=False)
    if 'SpiceBot_Logs' not in bot.memory:
        bot.memory['SpiceBot_Logs'] = {}

    if 'SpiceBot_Logs_queue' not in bot.memory:
        bot.memory['SpiceBot_Logs_queue'] = []


@sopel.module.event('001')
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):
    if bot.config.SpiceBot_Logs.logging_channel:
        channel = bot.config.SpiceBot_Logs.logging_channel
        if channel not in bot.channels.keys():
            bot.write(('JOIN', bot.nick, channel))
            if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                bot.write(('SAJOIN', bot.nick, channel))

    while True:
        if len(bot.memory['SpiceBot_Logs_queue']):
            bot.say(str(bot.memory['SpiceBot_Logs_queue'][0]))
            del bot.memory['SpiceBot_Logs_queue'][0]


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
