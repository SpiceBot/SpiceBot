# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot events system.

We utilize the Sopel code for event numbers and
self-trigger the bot into performing actions
"""


import sopel
import functools


class BotEvents(object):
    """A dynamic listing of all the notable Bot numeric events.

    Events will be assigned a 4-digit number above 1000.

    This allows you to do, ``@module.event(botevents.BOT_WELCOME)````

    Triggers handled by this module will be processed immediately.
    Others will be placed into a queue.

    Triggers will be logged by ID and content
    """

    def __init__(self):
        self.RPL_WELCOME = '001'  # This is a defined IRC event
        self.BOT_WELCOME = '1001'
        self.BOT_READY = '1002'
        self.BOT_CONNECTED = '1003'
        self.BOT_LOADED = '1004'
        self.defaultevents = [self.BOT_WELCOME, self.BOT_READY, self.BOT_CONNECTED, self.BOT_LOADED]
        self.SpiceBot_Events = {
                                "assigned_IDs": [1000, 1001, 1002, 1003, 1004],
                                "triggers_recieved": {},
                                "trigger_queue": [],
                                "startup_required": [self.BOT_WELCOME, self.BOT_READY, self.BOT_CONNECTED]
                                }

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        eventnumber = max(self.SpiceBot_Events["assigned_IDs"]) + 1
        self.SpiceBot_Events["assigned_IDs"].append(eventnumber)
        setattr(self, name, str(eventnumber))
        return str(eventnumber)

    def trigger(self, bot, number, message="SpiceBot_Events"):
        number = str(number)
        if number in self.defaultevents or self.check(self.BOT_CONNECTED):
            pretrigger = sopel.trigger.PreTrigger(
                bot.nick,
                ":SpiceBot_Events " + number + " " + str(bot.nick) + " :" + message
            )
            bot.dispatch(pretrigger)
            self.recieved({"number": number, "message": message})
        else:
            pretriggerdict = {"number": number, "message": message}
            self.SpiceBot_Events["trigger_queue"].append(pretriggerdict)

    def recieved(self, trigger):
        if isinstance(trigger, dict):
            eventnumber = str(trigger["number"])
            message = str(trigger["message"])
        else:
            eventnumber = str(trigger.event)
            message = trigger.args[1]
        if eventnumber not in self.SpiceBot_Events["triggers_recieved"]:
            self.SpiceBot_Events["triggers_recieved"][eventnumber] = []
        self.SpiceBot_Events["triggers_recieved"][eventnumber].append(message)

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

    def check_ready(self, checklist):
        def actual_decorator(function):
            @functools.wraps(function)
            def _nop(*args, **kwargs):
                while not self.check(checklist):
                    pass
                return function(*args, **kwargs)
            return _nop
        return actual_decorator

    def startup_check_ready(self):
        def actual_decorator(function):
            @functools.wraps(function)
            def _nop(*args, **kwargs):
                while not self.startup_check():
                    pass
                return function(*args, **kwargs)
            return _nop
        return actual_decorator


botevents = BotEvents()
