#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel
from sopel.trigger import PreTrigger

from sopel_modules.SpiceBot_SBTools import bot_logging

from random import randint


class botevents(object):
    """An dynamic listing of all the notable Bot numeric events.

    Events contained in this module will utilize the 1000-range

    All Other events will be tagged with a randomly generated
    4-digit number above 2000.

    This allows you to do, for example, ``@module.event(botevents.BOT_WELCOME)``
    rather than ``@module.event('1001')``
    """

    usednumbers = [0, 1001, 1002, 1003, 1004, 2000]

    BOT_WELCOME = '1001'
    BOT_READY = '1002'
    BOT_CONNECTED = '1003'
    BOT_LOADED = '1004'

    def __getattr__(self, attr):
        ''' will only get called for undefined attributes '''
        eventnumber = max(self.usednumbers) + 1
        self.usednumbers.append(eventnumber)
        setattr(self, str(attr).upper()) = str(eventnumber)


def setup(bot):
    bot_logging(bot, 'SpiceBot_Events', "Starting setup procedure")
    bot_events_setup_check(bot)
    bot_events_startup_register(bot, [botevents.BOT_WELCOME, botevents.BOT_READY, botevents.BOT_CONNECTED])


def shutdown(bot):
    if "SpiceBot_Events" in bot.memory:
        del bot.memory["SpiceBot_Events"]


def bot_events_trigger(bot, number, message):

    bot_events_setup_check(bot)

    bot.memory["SpiceBot_Events"]["triggers"][str(number)] = message
    if str(number) in [botevents.BOT_WELCOME, botevents.BOT_READY, botevents.BOT_CONNECTED]:
        pretrigger = PreTrigger(
            bot.nick,
            ":SpiceBot_Events " + str(number) + " " + str(bot.nick) + " :" + message
        )
        bot.dispatch(pretrigger)
    else:
        pretriggerdict = {"number": number, "message": message}
        bot.memory['SpiceBot_Events']["queue"].append(pretriggerdict)


def bot_events_setup_check(bot):
    if "SpiceBot_Events" not in bot.memory:
        bot.memory["SpiceBot_Events"] = {"triggers": {}, "startup": [], "loaded": [], "queue": []}


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

    notcomplete = []

    for startupitem in bot.memory["SpiceBot_Events"]["startup"]:
        if str(startupitem) not in bot.memory["SpiceBot_Events"]["loaded"]:
            notcomplete.append(str(startupitem))

    if len(notcomplete):
        return False
    else:
        return True
