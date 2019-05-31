# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot events system.

We utilize the Sopel code for event numbers and
self-trigger the bot into performing actions
"""

import sopel
import functools
import threading
import time

from .Logs import logs


# TODO
# full_message = ':{} PRIVMSG {} :{}'.format(hostmask, sender, msg)


class BotEvents(object):
    """A dynamic listing of all the notable Bot numeric events.

    Events will be assigned a 4-digit number above 1000.

    This allows you to do, ``@module.event(events.BOT_WELCOME)````

    Triggers handled by this module will be processed immediately.
    Others will be placed into a queue.

    Triggers will be logged by ID and content
    """

    def __init__(self):
        self.lock = threading.Lock()
        self.RPL_WELCOME = '001'  # This is a defined IRC event
        self.BOT_UPTIME = time.time()
        self.BOT_WELCOME = '1001'
        self.BOT_READY = '1002'
        self.BOT_CONNECTED = '1003'
        self.BOT_LOADED = '1004'
        self.BOT_RECONNECTED = '1005'
        self.defaultevents = [self.BOT_WELCOME, self.BOT_READY, self.BOT_CONNECTED, self.BOT_LOADED, self.BOT_RECONNECTED]
        self.dict = {
                    "assigned_IDs": {1000: "BOT_UPTIME", 1001: "BOT_WELCOME", 1002: "BOT_READY", 1003: "BOT_CONNECTED", 1004: "BOT_LOADED", 1005: "BOT_RECONNECTED"},
                    "triggers_recieved": {},
                    "trigger_queue": [],
                    "startup_required": [self.BOT_WELCOME, self.BOT_READY, self.BOT_CONNECTED],
                    "RPL_WELCOME_Count": 0
                    }

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        self.lock.acquire()
        eventnumber = max(list(self.dict["assigned_IDs"].keys())) + 1
        self.dict["assigned_IDs"][eventnumber] = str(name)
        setattr(self, name, str(eventnumber))
        self.lock.release()
        return str(eventnumber)

    def trigger(self, bot, number, message="SpiceBot_Events"):
        pretriggerdict = {"number": str(number), "message": message}
        if number in self.defaultevents:
            self.dispatch(bot, pretriggerdict)
        else:
            self.dict["trigger_queue"].append(pretriggerdict)

    def dispatch(self, bot, pretriggerdict):
        number = pretriggerdict["number"]
        message = pretriggerdict["message"]
        pretrigger = sopel.trigger.PreTrigger(
            bot.nick,
            ":SpiceBot_Events " + str(number) + " " + str(bot.nick) + " :" + message
        )
        bot.dispatch(pretrigger)
        self.recieved({"number": number, "message": message})

    def recieved(self, trigger):
        self.lock.acquire()

        if isinstance(trigger, dict):
            eventnumber = str(trigger["number"])
            message = str(trigger["message"])
        else:
            eventnumber = str(trigger.event)
            message = trigger.args[1]
        if int(eventnumber) in self.defaultevents:
            logs.log('SpiceBot_Events', str(eventnumber) + "    " + str(message), True)
        else:
            logs.log('SpiceBot_Events', str(eventnumber) + "    " + str(message))
        if eventnumber not in self.dict["triggers_recieved"]:
            self.dict["triggers_recieved"][eventnumber] = []
        self.dict["triggers_recieved"][eventnumber].append(message)
        self.lock.release()

    def check(self, checklist):
        if not isinstance(checklist, list):
            checklist = [str(checklist)]
        for number in checklist:
            if str(number) not in self.dict["triggers_recieved"].keys():
                return False
        return True

    def startup_add(self, startlist):
        self.lock.acquire()
        if not isinstance(startlist, list):
            startlist = [str(startlist)]
        self.dict["startup_required"].extend(startlist)
        self.lock.release()

    def startup_check(self):
        for number in self.dict["startup_required"]:
            if str(number) not in self.dict["triggers_recieved"].keys():
                return False
        return True

    def startup_debug(self):
        not_done = []
        for number in self.dict["startup_required"]:
            if str(number) not in self.dict["triggers_recieved"].keys():
                not_done.append(int(number))
        reference_not_done = []
        for item in not_done:
            reference_not_done.append(str(self.dict["assigned_IDs"][item]))
        return reference_not_done

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


events = BotEvents()
