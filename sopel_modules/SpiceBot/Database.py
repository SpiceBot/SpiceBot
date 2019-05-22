# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Database
"""

from sopel.tools import Identifier

import threading


class BotDatabase():
    """A thread safe database cache"""

    def __init__(self):
        self.lock = threading.Lock()
        self.SpiceBot_Database = {
                                "nicks": {},
                                "channels": {},
                                }

    """Nick"""

    def get_nick_value(self, bot, nick, key, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = bot.db.get_nick_id(nick, create=True)

        if nick_id not in self.SpiceBot_Database["nicks"].keys():
            self.SpiceBot_Database["nicks"][nick_id] = {}

        if sorting_key not in self.SpiceBot_Database["nicks"][nick_id].keys():
            self.SpiceBot_Database["nicks"][nick_id][sorting_key] = bot.db.get_nick_value(nick, sorting_key) or dict()

        self.lock.release()

        if key not in self.SpiceBot_Database["nicks"][nick_id][sorting_key].keys():
            return None
        else:
            return self.SpiceBot_Database["nicks"][nick_id][sorting_key][key]

    def set_nick_value(self, bot, nick, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = bot.db.get_nick_id(nick, create=True)

        if nick_id not in self.SpiceBot_Database["nicks"].keys():
            self.SpiceBot_Database["nicks"][nick_id] = {}
            self.lock.release()

        if sorting_key not in self.SpiceBot_Database["nicks"][nick_id].keys():
            self.SpiceBot_Database["nicks"][nick_id][sorting_key] = bot.db.get_nick_value(nick, sorting_key) or dict()
            self.lock.release()

        self.SpiceBot_Database["nicks"][nick_id][sorting_key][key] = value

        bot.db.set_nick_value(nick, sorting_key, self.SpiceBot_Database["nicks"][nick_id][sorting_key])

        self.lock.release()

    def delete_nick_value(self, bot, nick, key, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = bot.db.get_nick_id(nick, create=True)

        if nick_id not in self.SpiceBot_Database["nicks"].keys():
            self.SpiceBot_Database["nicks"][nick_id] = {}

        if sorting_key not in self.SpiceBot_Database["nicks"][nick_id].keys():
            self.SpiceBot_Database["nicks"][nick_id][sorting_key] = bot.db.get_nick_value(nick, sorting_key) or dict()

        del self.SpiceBot_Database["nicks"][nick_id][sorting_key][key]
        bot.db.set_nick_value(nick, sorting_key, self.SpiceBot_Database["nicks"][nick_id][sorting_key])

        self.lock.release()

    def adjust_nick_value(self, bot, nick, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = bot.db.get_nick_id(nick, create=True)

        if nick_id not in self.SpiceBot_Database["nicks"].keys():
            self.SpiceBot_Database["nicks"][nick_id] = {}

        if sorting_key not in self.SpiceBot_Database["nicks"][nick_id].keys():
            self.SpiceBot_Database["nicks"][nick_id][sorting_key] = bot.db.get_nick_value(nick, sorting_key) or dict()

        if key not in self.SpiceBot_Database["nicks"][nick_id][sorting_key].keys():
            oldvalue = []
        else:
            oldvalue = self.SpiceBot_Database["nicks"][nick_id][sorting_key][key]

        if not oldvalue:
            self.SpiceBot_Database["nicks"][nick_id][sorting_key][key] = value
        else:
            self.SpiceBot_Database["nicks"][nick_id][sorting_key][key] = oldvalue + value
        bot.db.set_nick_value(nick, sorting_key, self.SpiceBot_Database["nicks"][nick_id][sorting_key])

        self.lock.release()

    def adjust_nick_list(self, bot, nick, key, entries, adjustmentdirection, sorting_key='unsorted'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        nick = Identifier(nick)
        nick_id = bot.db.get_nick_id(nick, create=True)

        if nick_id not in self.SpiceBot_Database["nicks"].keys():
            self.SpiceBot_Database["nicks"][nick_id] = {}

        if sorting_key not in self.SpiceBot_Database["nicks"][nick_id].keys():
            self.SpiceBot_Database["nicks"][nick_id][sorting_key] = bot.db.get_nick_value(nick, sorting_key) or dict()

        if key not in self.SpiceBot_Database["nicks"][nick_id][sorting_key].keys():
            self.SpiceBot_Database["nicks"][nick_id][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.SpiceBot_Database["nicks"][nick_id][sorting_key][key]:
                    self.SpiceBot_Database["nicks"][nick_id][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.SpiceBot_Database["nicks"][nick_id][sorting_key][key]:
                    self.SpiceBot_Database["nicks"][nick_id][sorting_key][key].remove(entry)
        bot.db.set_nick_value(nick, sorting_key, self.SpiceBot_Database["nicks"][nick_id][sorting_key])

        self.lock.release()

    """Channels"""

    def get_channel_value(self, bot, channel, key, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel)

        if channel not in self.SpiceBot_Database["channels"].keys():
            self.SpiceBot_Database["channels"][channel] = {}

        if sorting_key not in self.SpiceBot_Database["channels"][channel].keys():
            self.SpiceBot_Database["channels"][channel][sorting_key] = bot.db.get_channel_value(channel, sorting_key) or dict()

        self.lock.release()

        if key not in self.SpiceBot_Database["channels"][channel][sorting_key].keys():
            return None
        else:
            return self.SpiceBot_Database["channels"][channel][sorting_key][key]

    def set_channel_value(self, bot, channel, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel)

        if channel not in self.SpiceBot_Database["channels"].keys():
            self.SpiceBot_Database["channels"][channel] = {}

        if sorting_key not in self.SpiceBot_Database["channels"][channel].keys():
            self.SpiceBot_Database["channels"][channel][sorting_key] = bot.db.get_channel_value(channel, sorting_key) or dict()

        self.SpiceBot_Database["channels"][channel][sorting_key][key] = value
        bot.db.set_channel_value(channel, sorting_key, self.SpiceBot_Database["channels"][channel][sorting_key])

        self.lock.release()

    def delete_channel_value(self, bot, channel, key, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel)

        if channel not in self.SpiceBot_Database["channels"].keys():
            self.SpiceBot_Database["channels"][channel] = {}

        if sorting_key not in self.SpiceBot_Database["channels"][channel].keys():
            self.SpiceBot_Database["channels"][channel][sorting_key] = bot.db.get_channel_value(channel, sorting_key) or dict()

        del self.SpiceBot_Database["channels"][channel][sorting_key][key]
        bot.db.set_channel_value(channel, sorting_key, self.SpiceBot_Database["channels"][channel][sorting_key])

        self.lock.release()

    def adjust_channel_value(self, bot, channel, key, value, sorting_key='unsorted'):

        self.lock.acquire()

        channel = Identifier(channel)

        if channel not in self.SpiceBot_Database["channels"].keys():
            self.SpiceBot_Database["channels"][channel] = {}

        if sorting_key not in self.SpiceBot_Database["channels"][channel].keys():
            self.SpiceBot_Database["channels"][channel][sorting_key] = bot.db.get_channel_value(channel, sorting_key) or dict()

        if key not in self.SpiceBot_Database["channels"][channel][sorting_key].keys():
            oldvalue = None
        else:
            oldvalue = self.SpiceBot_Database["channels"][channel][sorting_key][key]

        if not oldvalue:
            self.SpiceBot_Database["channels"][channel][sorting_key][key] = value
        else:
            self.SpiceBot_Database["channels"][channel][sorting_key][key] = oldvalue + value
        bot.db.set_channel_value(channel, sorting_key, self.SpiceBot_Database["channels"][channel][sorting_key])

        self.lock.release()

    def adjust_channel_list(self, bot, channel, key, entries, adjustmentdirection, sorting_key='unsorted'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        channel = Identifier(channel)

        if channel not in self.SpiceBot_Database["channels"].keys():
            self.SpiceBot_Database["channels"][channel] = {}

        if sorting_key not in self.SpiceBot_Database["channels"][channel].keys():
            self.SpiceBot_Database["channels"][channel][sorting_key] = bot.db.get_channel_value(channel, sorting_key) or dict()

        if key not in self.SpiceBot_Database["channels"][channel][sorting_key].keys():
            self.SpiceBot_Database["channels"][channel][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.SpiceBot_Database["channels"][channel][sorting_key][key]:
                    self.SpiceBot_Database["channels"][channel][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.SpiceBot_Database["channels"][channel][sorting_key][key]:
                    self.SpiceBot_Database["channels"][channel][sorting_key][key].remove(entry)
        bot.db.set_channel_value(channel, sorting_key, self.SpiceBot_Database["channels"][channel][sorting_key])

        self.lock.release()
