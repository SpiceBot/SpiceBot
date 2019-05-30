# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Database
"""

# sopel imports
from sopel.tools import Identifier
import sopel.db
from sopel.db import SopelDB, _deserialize, NickValues, ChannelValues

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
    category = Column(String(255), primary_key=True)
    key = Column(String(255))
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
                result.value = float(result.value) + float(value)
                session.commit()
            # DNE - Insert
            else:
                new_nickvalue = NickValues(nick_id=nick_id, key=key, value=float(value))
                session.add(new_nickvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_nick_list(self, nick, key, entries, adjustmentdirection):
        """Sets the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        if not isinstance(entries, list):
            entries = [entries]
        entries = json.dumps(entries, ensure_ascii=False)
        nick_id = self.get_nick_id(nick)
        session = self.ssession()
        try:
            result = session.query(NickValues) \
                .filter(NickValues.nick_id == nick_id) \
                .filter(NickValues.key == key) \
                .one_or_none()
            # NickValue exists, update
            if result:
                if adjustmentdirection == 'add':
                    for entry in entries:
                        if entry not in result.value:
                            result.value.append(entry)
                elif adjustmentdirection == 'del':
                    for entry in entries:
                        while entry in result.value:
                            result.value.remove(entry)
                session.commit()
            # DNE - Insert
            else:
                values = []
                if adjustmentdirection == 'add':
                    for entry in entries:
                        if entry not in values:
                            values.append(entry)
                elif adjustmentdirection == 'del':
                    for entry in entries:
                        while entry in values:
                            values.remove(entry)
                new_nickvalue = NickValues(nick_id=nick_id, key=key, value=values)
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
                result.value = float(result.value) + float(value)
                session.commit()
            # DNE - Insert
            else:
                new_channelvalue = ChannelValues(channel=channel, key=key, value=float(value))
                session.add(new_channelvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_channel_list(self, channel, key, entries, adjustmentdirection):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        if not isinstance(entries, list):
            entries = [entries]
        entries = json.dumps(entries, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                if adjustmentdirection == 'add':
                    for entry in entries:
                        if entry not in result.value:
                            result.value.append(entry)
                elif adjustmentdirection == 'del':
                    for entry in entries:
                        while entry in result.value:
                            result.value.remove(entry)
                session.commit()
            # DNE - Insert
            else:
                values = []
                if adjustmentdirection == 'add':
                    for entry in entries:
                        if entry not in values:
                            values.append(entry)
                elif adjustmentdirection == 'del':
                    for entry in entries:
                        while entry in values:
                            values.remove(entry)
                new_channelvalue = ChannelValues(channel=channel, key=key, value=values)
                session.add(new_channelvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    # PLUGIN FUNCTIONS

    def set_plugin_value(self, plugin, key, value, category='default'):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.category == category)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # PluginValues exists, update
            if result:
                result.value = value
                session.commit()
            # DNE - Insert
            else:
                new_pluginvalue = PluginValues(plugin=plugin, category=category, key=key, value=value)
                session.add(new_pluginvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_plugin_value(self, plugin, key, category='default'):
        """Retrieves the value for a given key associated with a plugin."""
        plugin = Identifier(plugin).lower()
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.category == category)\
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

    def delete_plugin_value(self, plugin, key, category='default'):
        """Deletes the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.category == category)\
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

    def adjust_plugin_value(self, plugin, key, value, category='default'):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.category == category)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                result.value = float(result.value) + float(value)
                session.commit()
            # DNE - Insert
            else:
                new_pluginvalue = PluginValues(plugin=plugin, category=category, key=key, value=float(value))
                session.add(new_pluginvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_plugin_list(self, plugin, key, entries, adjustmentdirection, category='default'):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        if not isinstance(entries, list):
            entries = [entries]
        entries = json.dumps(entries, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.category == category)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                if adjustmentdirection == 'add':
                    for entry in entries:
                        if entry not in result.value:
                            result.value.append(entry)
                elif adjustmentdirection == 'del':
                    for entry in entries:
                        while entry in result.value:
                            result.value.remove(entry)
                session.commit()
            # DNE - Insert
            else:
                values = []
                if adjustmentdirection == 'add':
                    for entry in entries:
                        if entry not in values:
                            values.append(entry)
                elif adjustmentdirection == 'del':
                    for entry in entries:
                        while entry in values:
                            values.remove(entry)
                new_pluginvalue = PluginValues(plugin=plugin, category=category, key=key, value=values)
                session.add(new_pluginvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()


class BotDatabase():
    """A thread safe database cache"""

    def __init__(self):

        SopelDB.delete_nick_value = SpiceDB.delete_nick_value
        SopelDB.adjust_nick_value = SpiceDB.adjust_nick_value
        SopelDB.adjust_nick_list = SpiceDB.adjust_nick_list

        SopelDB.delete_channel_value = SpiceDB.delete_channel_value
        SopelDB.adjust_channel_value = SpiceDB.adjust_channel_value
        SopelDB.adjust_channel_list = SpiceDB.adjust_channel_list

        sopel.db.PluginValues = PluginValues
        SopelDB.get_plugin_value = SpiceDB.get_plugin_value
        SopelDB.set_plugin_value = SpiceDB.set_plugin_value
        SopelDB.delete_plugin_value = SpiceDB.delete_plugin_value
        SopelDB.adjust_plugin_value = SpiceDB.adjust_plugin_value
        SopelDB.adjust_plugin_list = SpiceDB.adjust_plugin_list

        self.db = SopelDB(botconfig.config)

    """Nick"""

    def get_nick_value(self, nick, key):
        return self.db.get_nick_value(nick, key)

    def set_nick_value(self, nick, key, value):
        return self.db.set_nick_value(nick, key, value)

    def delete_nick_value(self, nick, key):
        return self.db.delete_nick_value(nick, key)

    def adjust_nick_value(self, nick, key, value):
        return self.db.adjust_nick_value(nick, key, value)

    def adjust_nick_list(self, nick, key, entries, adjustmentdirection):
        return self.db.adjust_nick_list(nick, key, entries, adjustmentdirection)

    """Bot"""

    def get_bot_value(self, key):
        return self.db.get_nick_value(botconfig.nick, key)

    def set_bot_value(self, key, value):
        return self.db.set_nick_value(botconfig.nick, key, value)

    def delete_bot_value(self, key):
        return self.db.delete_nick_value(botconfig.nick, key)

    def adjust_bot_value(self, key, value):
        return self.db.adjust_nick_value(botconfig.nick, key, value)

    def adjust_bot_list(self, key, entries, adjustmentdirection):
        return self.db.adjust_nick_list(botconfig.nick, key, entries, adjustmentdirection)

    """Channels"""

    def get_channel_value(self, channel, key):
        return self.db.get_channel_value(channel, key)

    def set_channel_value(self, channel, key, value):
        return self.db.set_channel_value(channel, key, value)

    def delete_channel_value(self, channel, key):
        return self.db.delete_channel_value(channel, key)

    def adjust_channel_value(self, channel, key, value):
        return self.db.adjust_channel_value(channel, key, value)

    def adjust_channel_list(self, nick, key, entries, adjustmentdirection):
        return self.db.adjust_channel_list(nick, key, entries, adjustmentdirection)

    """Plugins"""

    def get_plugin_value(self, plugin, key):
        return self.db.get_plugin_value(plugin, key)

    def set_plugin_value(self, plugin, key, value):
        return self.db.set_plugin_value(plugin, key, value)

    def delete_plugin_value(self, plugin, key):
        return self.db.delete_plugin_value(plugin, key)

    def adjust_plugin_value(self, plugin, key, value):
        return self.db.adjust_plugin_value(plugin, key, value)

    def adjust_plugin_list(self, nick, key, entries, adjustmentdirection):
        return self.db.adjust_plugin_list(nick, key, entries, adjustmentdirection)


db = BotDatabase()
