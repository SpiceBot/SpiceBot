#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel
from sopel.trigger import PreTrigger
# import functools

from sopel_modules.SpiceBot_SBTools import bot_logging


class BotEvents(object):
    """A dynamic listing of all the notable Bot numeric events.

    Events will be assigned a 4-digit number above 1000.

    This allows you to do, ``@module.event(botevents.BOT_WELCOME)````
    """

    def __init__(self):
        self.SpiceBot_Events = {"assigned_IDs": [1000]}

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        eventnumber = max(self.SpiceBot_Events["assigned_IDs"]) + 1
        self.SpiceBot_Events["assigned_IDs"].append(eventnumber)
        setattr(self, name, str(eventnumber))
        return str(eventnumber)


botevents = BotEvents()


"""
def register_trigger(number, message):
    def actual_decorator(function):
        @functools.wraps(function)
        def _nop(*args, **kwargs):
            # Assign trigger and bot for easy access later
            bot, trigger = args[0:2]
            return function(*args, **kwargs)
        return _nop
"""


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
