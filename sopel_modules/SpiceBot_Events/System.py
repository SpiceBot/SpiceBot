#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel

from sopel_modules.SpiceBot_SBTools import bot_logging


def setup(bot):
    bot_logging(bot, 'SpiceBot_Events', "Starting setup procedure")
    bot_events_setup_check(bot)
    bot_events_startup_register(bot, ['1001', '1002', '1003'])


def shutdown(bot):
    if "SpiceBot_Events" in bot.memory:
        del bot.memory["SpiceBot_Events"]


def bot_events_trigger(bot, number, message):

    bot_events_setup_check(bot)

    bot.memory["SpiceBot_Events"]["triggers"][str(number)] = message

    pretrigger = sopel.trigger.PreTrigger(
        bot.nick,
        ":SpiceBot_Events " + str(number) + " " + str(bot.nick) + " :" + message
    )
    bot.dispatch(pretrigger)


def bot_events_setup_check(bot):
    if "SpiceBot_Events" not in bot.memory:
        bot.memory["SpiceBot_Events"] = {"triggers": {}, "startup": [], "loaded": []}


def bot_events_check(bot, listreq):

    bot_events_setup_check(bot)

    if not isinstance(listreq, list):
        listreq = [str(listreq)]

    for requirement in listreq:
        if requirement not in bot.memory["SpiceBot_Events"]["loaded"]:
            return False

    return True


def bot_events_startup_register(bot, addonreq):

    bot_events_setup_check(bot)

    if not isinstance(addonreq, list):
        addonreq = [str(addonreq)]

    bot.memory["SpiceBot_Events"]["startup"].extend(addonreq)


def bot_events_recieved(bot, number):

    bot_events_setup_check(bot)

    if str(number) not in bot.memory["SpiceBot_Events"]["loaded"]:
        bot.memory["SpiceBot_Events"]["loaded"].append(str(number))


def bot_events_startup_check(bot):

    bot_events_setup_check(bot)

    for startupitem in bot.memory["SpiceBot_Events"]["startup"]:
        if str(startupitem) not in bot.memory["SpiceBot_Events"]["loaded"]:
            bot_logging(bot, 'SpiceBot_Events', str(startupitem))
            return False

    return True
