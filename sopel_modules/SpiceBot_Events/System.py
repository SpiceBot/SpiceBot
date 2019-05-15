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

    Triggers handled by this module will be processed immediately.
    Others will be placed into a queue.

    Triggers will be logged by ID and content
    """

    def __init__(self):
        self.SpiceBot_Events = {
                                "assigned_IDs": [1000],
                                "triggers_recieved": {},
                                "trigger_queue": [],
                                "startup_required": []
                                }

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        eventnumber = max(self.SpiceBot_Events["assigned_IDs"]) + 1
        self.SpiceBot_Events["assigned_IDs"].append(eventnumber)
        setattr(self, name, str(eventnumber))
        return str(eventnumber)

    def trigger(self, bot, number, message="SpiceBot_Events"):
        number = str(number)
        if number in [self.BOT_WELCOME, self.BOT_READY, self.BOT_CONNECTED, self.BOT_LOADED]:
            pretrigger = PreTrigger(
                bot.nick,
                ":SpiceBot_Events " + number + " " + str(bot.nick) + " :" + message
            )
            bot.dispatch(pretrigger)
        else:
            pretriggerdict = {"number": number, "message": message}
            self.SpiceBot_Events["trigger_queue"].append(pretriggerdict)

    def recieved(self, trigger):
        eventnumber = str(trigger.event)
        message_payload = trigger.args[1]
        if eventnumber not in self.SpiceBot_Events["triggers_recieved"]:
            self.SpiceBot_Events["triggers_recieved"][eventnumber] = []
        self.SpiceBot_Events["assigned_IDs"]["triggers_recieved"][eventnumber].append(message_payload)

    def check(self, checklist):
        if not isinstance(checklist, list):
            checklist = [str(checklist)]
        for number in checklist:
            if str(number) not in self.SpiceBot_Events["triggers_recieved"].keys():
                return False
        return True

    def startup_add(self, startlist):
        if not isinstance(startlist, list):
            startlist = [str(startlist)]
        self.SpiceBot_Events["startup_required"].extend(startlist)

    def startup_check(self):
        for number in self.SpiceBot_Events["startup_required"]:
            if str(number) not in self.SpiceBot_Events["triggers_recieved"].keys():
                return False
        return True


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

ideas:

    while not botevents.check([botevents.BOT_LOADED, botevents.BOT_COMMANDSQUERY]):
        pass

"""


def setup(bot):
    bot_logging(bot, 'SpiceBot_Events', "Starting setup procedure")
    botevents.startup_add([botevents.BOT_WELCOME, botevents.BOT_READY, botevents.BOT_CONNECTED])
