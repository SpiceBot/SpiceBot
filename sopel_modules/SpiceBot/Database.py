# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Database
"""

# sopel imports
from sopel.tools import Identifier
import sopel.db
from sopel.db import SopelDB, _deserialize, NickValues, ChannelValues

import threading
from .Config import config as botconfig

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

import json


BASE = declarative_base()


class PluginValues(BASE):
    """
    PluginValues SQLAlchemy Class
    """
    __tablename__ = 'plugin_values'
    plugin = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(String(255))


class SpiceDB(object):

    # NICK FUNCTIONS

    def delete_nick_value(self, nick, key):
        """Deletes the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        nick_id = self.get_nick_id(nick)
        session = self.ssession()
        try:
            result = session.query(NickValues) \
                .filter(NickValues.nick_id == nick_id) \
                .filter(NickValues.key == key) \
                .one_or_none()
            # NickValue exists, delete
            if result:
                session.delete(result)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_nick_value(self, nick, key, value):
        """Sets the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        value = json.dumps(value, ensure_ascii=False)
        nick_id = self.get_nick_id(nick)
        session = self.ssession()
        try:
            result = session.query(NickValues) \
                .filter(NickValues.nick_id == nick_id) \
                .filter(NickValues.key == key) \
                .one_or_none()
            # NickValue exists, update
            if result:
                result.value = result.value + value
                session.commit()
            # DNE - Insert
            else:
                new_nickvalue = NickValues(nick_id=nick_id, key=key, value=value)
                session.add(new_nickvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    # CHANNEL FUNCTIONS

    def delete_channel_value(self, channel, key):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.key == key) \
                .one_or_none()
            # ChannelValue exists, delete
            if result:
                session.delete(result)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_channel_value(self, channel, key, value):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                result.value = result.value + value
                session.commit()
            # DNE - Insert
            else:
                new_channelvalue = ChannelValues(channel=channel, key=key, value=value)
                session.add(new_channelvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    # PLUGIN FUNCTIONS

    def set_plugin_value(self, plugin, key, value):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # PluginValues exists, update
            if result:
                result.value = value
                session.commit()
            # DNE - Insert
            else:
                new_pluginvalue = PluginValues(plugin=plugin, key=key, value=value)
                session.add(new_pluginvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_plugin_value(self, plugin, key):
        """Retrieves the value for a given key associated with a plugin."""
        plugin = Identifier(plugin).lower()
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            if result is not None:
                result = result.value
            return _deserialize(result)
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_plugin_value(self, plugin, key, value):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                result.value = result.value + value
                session.commit()
            # DNE - Insert
            else:
                new_pluginvalue = PluginValues(plugin=plugin, key=key, value=value)
                session.add(new_pluginvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_plugin_value(self, plugin, key):
        """Deletes the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # PluginValues exists, delete
            if result:
                session.delete(result)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()


class BotDatabase():
    """A thread safe database cache"""

    def __init__(self):
        self.lock = threading.Lock()
        self.dict = {
                    "nicks": {},
                    "channels": {},
                    }

        SopelDB.delete_nick_value = SpiceDB.delete_nick_value
        SopelDB.adjust_nick_value = SpiceDB.adjust_nick_value

        SopelDB.delete_channel_value = SpiceDB.delete_channel_value
        SopelDB.adjust_channel_value = SpiceDB.adjust_channel_value

        sopel.db.PluginValues = PluginValues
        SopelDB.get_plugin_value = SpiceDB.get_plugin_value
        SopelDB.set_plugin_value = SpiceDB.set_plugin_value
        SopelDB.delete_plugin_value = SpiceDB.delete_plugin_value
        SopelDB.adjust_plugin_value = SpiceDB.adjust_plugin_value

        self.db = SopelDB(botconfig.config)

    """Nick"""

    def get_nick_value(self, nick, key, sorting_key='defaultindex'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        self.lock.release()

        if key not in self.dict["nicks"][nick_id][sorting_key].keys():
            return None
        else:
            return self.dict["nicks"][nick_id][sorting_key][key]

    def set_nick_value(self, nick, key, value, sorting_key='defaultindex'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        self.dict["nicks"][nick_id][sorting_key][key] = value

        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    def delete_nick_value(self, nick, key, sorting_key='defaultindex'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        del self.dict["nicks"][nick_id][sorting_key][key]
        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    def adjust_nick_value(self, nick, key, value, sorting_key='defaultindex'):

        self.lock.acquire()

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        if key not in self.dict["nicks"][nick_id][sorting_key].keys():
            oldvalue = []
        else:
            oldvalue = self.dict["nicks"][nick_id][sorting_key][key]

        if not oldvalue:
            self.dict["nicks"][nick_id][sorting_key][key] = value
        else:
            self.dict["nicks"][nick_id][sorting_key][key] = oldvalue + value
        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    def adjust_nick_list(self, nick, key, entries, adjustmentdirection, sorting_key='defaultindex'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        nick = Identifier(nick)
        nick_id = self.db.get_nick_id(nick, create=True)

        if nick_id not in self.dict["nicks"].keys():
            self.dict["nicks"][nick_id] = {}

        if sorting_key not in self.dict["nicks"][nick_id].keys():
            self.dict["nicks"][nick_id][sorting_key] = self.db.get_nick_value(nick, sorting_key) or dict()

        if key not in self.dict["nicks"][nick_id][sorting_key].keys():
            self.dict["nicks"][nick_id][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.dict["nicks"][nick_id][sorting_key][key]:
                    self.dict["nicks"][nick_id][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.dict["nicks"][nick_id][sorting_key][key]:
                    self.dict["nicks"][nick_id][sorting_key][key].remove(entry)
        self.db.set_nick_value(nick, sorting_key, self.dict["nicks"][nick_id][sorting_key])

        self.lock.release()

    """Bot"""

    def get_bot_value(self, key, sorting_key='defaultindex'):
        return self.get_nick_value(botconfig.nick, key, sorting_key)

    def set_bot_value(self, key, value, sorting_key='defaultindex'):
        return self.set_nick_value(botconfig.nick, key, value, sorting_key)

    def delete_bot_value(self, key, sorting_key='defaultindex'):
        return self.delete_nick_value(botconfig.nick, key, sorting_key)

    def adjust_bot_value(self, key, value, sorting_key='defaultindex'):
        return self.adjust_nick_value(botconfig.nick, key, value, sorting_key)

    def adjust_bot_list(self, key, entries, adjustmentdirection, sorting_key):
        return self.adjust_nick_list(botconfig.nick, key, entries, adjustmentdirection, sorting_key)

    """Channels"""

    def get_channel_value(self, channel, key, sorting_key='defaultindex'):

        self.lock.acquire()

        channel = Identifier(channel).lower().lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        self.lock.release()

        if key not in self.dict["channels"][channel][sorting_key].keys():
            return None
        else:
            return self.dict["channels"][channel][sorting_key][key]

    def set_channel_value(self, channel, key, value, sorting_key='defaultindex'):

        self.lock.acquire()

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        self.dict["channels"][channel][sorting_key][key] = value
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    def delete_channel_value(self, channel, key, sorting_key='defaultindex'):

        self.lock.acquire()

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        del self.dict["channels"][channel][sorting_key][key]
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    def adjust_channel_value(self, channel, key, value, sorting_key='defaultindex'):

        self.lock.acquire()

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        if key not in self.dict["channels"][channel][sorting_key].keys():
            oldvalue = None
        else:
            oldvalue = self.dict["channels"][channel][sorting_key][key]

        if not oldvalue:
            self.dict["channels"][channel][sorting_key][key] = value
        else:
            self.dict["channels"][channel][sorting_key][key] = oldvalue + value
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    def adjust_channel_list(self, channel, key, entries, adjustmentdirection, sorting_key='defaultindex'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        channel = Identifier(channel).lower()

        if channel not in self.dict["channels"].keys():
            self.dict["channels"][channel] = {}

        if sorting_key not in self.dict["channels"][channel].keys():
            self.dict["channels"][channel][sorting_key] = self.db.get_channel_value(channel, sorting_key) or dict()

        if key not in self.dict["channels"][channel][sorting_key].keys():
            self.dict["channels"][channel][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.dict["channels"][channel][sorting_key][key]:
                    self.dict["channels"][channel][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.dict["channels"][channel][sorting_key][key]:
                    self.dict["channels"][channel][sorting_key][key].remove(entry)
        self.db.set_channel_value(channel, sorting_key, self.dict["channels"][channel][sorting_key])

        self.lock.release()

    """Plugins"""

    def get_plugin_value(self, plugin, key, sorting_key='defaultindex'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        self.lock.release()

        if key not in self.dict["plugins"][plugin][sorting_key].keys():
            return None
        else:
            return self.dict["plugins"][plugin][sorting_key][key]

    def set_plugin_value(self, plugin, key, value, sorting_key='defaultindex'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        self.dict["plugins"][plugin][sorting_key][key] = value
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()

    def delete_plugin_value(self, plugin, key, sorting_key='defaultindex'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        del self.dict["plugins"][plugin][sorting_key][key]
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()

    def adjust_plugin_value(self, plugin, key, value, sorting_key='defaultindex'):

        self.lock.acquire()

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        if key not in self.dict["plugins"][plugin][sorting_key].keys():
            oldvalue = None
        else:
            oldvalue = self.dict["plugins"][plugin][sorting_key][key]

        if not oldvalue:
            self.dict["plugins"][plugin][sorting_key][key] = value
        else:
            self.dict["plugins"][plugin][sorting_key][key] = oldvalue + value
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()

    def adjust_plugin_list(self, plugin, key, entries, adjustmentdirection, sorting_key='defaultindex'):

        self.lock.acquire()

        if not isinstance(entries, list):
            entries = [entries]

        plugin = plugin.lower()

        if plugin not in self.dict["plugins"].keys():
            self.dict["plugins"][plugin] = {}

        if sorting_key not in self.dict["plugins"][plugin].keys():
            self.dict["plugins"][plugin][sorting_key] = self.db.get_plugin_value(plugin, sorting_key) or dict()

        if key not in self.dict["plugins"][plugin][sorting_key].keys():
            self.dict["plugins"][plugin][sorting_key][key] = []

        if adjustmentdirection == 'add':
            for entry in entries:
                if entry not in self.dict["plugins"][plugin][sorting_key][key]:
                    self.dict["plugins"][plugin][sorting_key][key].append(entry)
        elif adjustmentdirection == 'del':
            for entry in entries:
                while entry in self.dict["plugins"][plugin][sorting_key][key]:
                    self.dict["plugins"][plugin][sorting_key][key].remove(entry)
        self.db.set_plugin_value(plugin, sorting_key, self.dict["plugins"][plugin][sorting_key])

        self.lock.release()


db = BotDatabase()
