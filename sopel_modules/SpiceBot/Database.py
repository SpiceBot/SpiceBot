# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Database
"""

# sopel imports
from sopel.tools import Identifier
import sopel.db
from sopel.db import SopelDB, _deserialize

from .Config import config as botconfig

from sqlalchemy import Column, String, ForeignKey, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

import json


BASE = declarative_base()


class NickIDs(BASE):
    """
    NickIDs SQLAlchemy Class
    """
    __tablename__ = 'spice_nick_ids'
    nick_id = Column(Integer, primary_key=True)


class Nicknames(BASE):
    """
    Nicknames SQLAlchemy Class
    """
    __tablename__ = 'nicknames'
    nick_id = Column(Integer, ForeignKey('spice_nick_ids.nick_id'), primary_key=True)
    slug = Column(String(255), primary_key=True)
    canonical = Column(String(255))


class NickValues(BASE):
    """
    NickValues SQLAlchemy Class
    """
    __tablename__ = 'spice_nick_values'
    nick_id = Column(Integer, ForeignKey('spice_nick_ids.nick_id'), primary_key=True)
    namespace = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(Text())


class ChannelValues(BASE):
    """
    ChannelValues SQLAlchemy Class
    """
    __tablename__ = 'spice_channel_values'
    channel = Column(String(255), primary_key=True)
    namespace = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(Text())


class PluginValues(BASE):
    """
    PluginValues SQLAlchemy Class
    """
    __tablename__ = 'spice_plugin_values'
    plugin = Column(String(255), primary_key=True)
    namespace = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(Text())


class SpiceDB(object):

    # NICK FUNCTIONS

    def set_nick_value(self, nick, key, value, namespace='default'):
        """Sets the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        value = json.dumps(value, ensure_ascii=False)
        nick_id = self.get_nick_id(nick)
        session = self.ssession()
        try:
            result = session.query(NickValues) \
                .filter(NickValues.nick_id == nick_id) \
                .filter(NickValues.namespace == namespace)\
                .filter(NickValues.key == key) \
                .one_or_none()
            # NickValue exists, update
            if result:
                result.value = value
                session.commit()
            # DNE - Insert
            else:
                new_nickvalue = NickValues(nick_id=nick_id, namespace=namespace, key=key, value=value)
                session.add(new_nickvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_nick_value(self, nick, key, namespace='default'):
        """Retrieves the value for a given key associated with a nick."""
        nick = Identifier(nick)
        session = self.ssession()
        try:
            result = session.query(NickValues) \
                .filter(Nicknames.nick_id == NickValues.nick_id) \
                .filter(Nicknames.slug == nick.lower()) \
                .filter(NickValues.namespace == namespace)\
                .filter(NickValues.key == key) \
                .one_or_none()
            if result is not None:
                result = result.value
            return _deserialize(result)
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_nick_value(self, nick, key, namespace='default'):
        """Deletes the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        nick_id = self.get_nick_id(nick)
        session = self.ssession()
        try:
            result = session.query(NickValues) \
                .filter(NickValues.nick_id == nick_id) \
                .filter(NickValues.namespace == namespace)\
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

    def adjust_nick_value(self, nick, key, value, namespace='default'):
        """Sets the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        value = json.dumps(value, ensure_ascii=False)
        nick_id = self.get_nick_id(nick)
        session = self.ssession()
        try:
            result = session.query(NickValues) \
                .filter(NickValues.nick_id == nick_id) \
                .filter(NickValues.namespace == namespace)\
                .filter(NickValues.key == key) \
                .one_or_none()
            # NickValue exists, update
            if result:
                result.value = float(result.value) + float(value)
                session.commit()
            # DNE - Insert
            else:
                new_nickvalue = NickValues(nick_id=nick_id, namespace=namespace, key=key, value=float(value))
                session.add(new_nickvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_nick_list(self, nick, key, entries, adjustmentdirection, namespace='default'):
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
                .filter(NickValues.namespace == namespace)\
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
                new_nickvalue = NickValues(nick_id=nick_id, namespace=namespace, key=key, value=values)
                session.add(new_nickvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    # CHANNEL FUNCTIONS

    def set_channel_value(self, channel, key, value, namespace='default'):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.namespace == namespace)\
                .filter(ChannelValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                result.value = value
                session.commit()
            # DNE - Insert
            else:
                new_channelvalue = ChannelValues(channel=channel, namespace=namespace, key=key, value=value)
                session.add(new_channelvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_channel_value(self, channel, key, namespace='default'):
        """Retrieves the value for a given key associated with a channel."""
        channel = Identifier(channel).lower()
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.namespace == namespace)\
                .filter(ChannelValues.key == key) \
                .one_or_none()
            if result is not None:
                result = result.value
            return _deserialize(result)
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_channel_value(self, channel, key, namespace='default'):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.namespace == namespace)\
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

    def adjust_channel_value(self, channel, key, value, namespace='default'):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.namespace == namespace)\
                .filter(ChannelValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                result.value = float(result.value) + float(value)
                session.commit()
            # DNE - Insert
            else:
                new_channelvalue = ChannelValues(channel=channel, namespace=namespace, key=key, value=float(value))
                session.add(new_channelvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_channel_list(self, channel, key, entries, adjustmentdirection, namespace='default'):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        if not isinstance(entries, list):
            entries = [entries]
        entries = json.dumps(entries, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.namespace == namespace)\
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
                new_channelvalue = ChannelValues(channel=channel, namespace=namespace, key=key, value=values)
                session.add(new_channelvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    # PLUGIN FUNCTIONS

    def set_plugin_value(self, plugin, key, value, namespace='default'):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.namespace == namespace)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # PluginValues exists, update
            if result:
                result.value = value
                session.commit()
            # DNE - Insert
            else:
                new_pluginvalue = PluginValues(plugin=plugin, namespace=namespace, key=key, value=value)
                session.add(new_pluginvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_plugin_value(self, plugin, key, namespace='default'):
        """Retrieves the value for a given key associated with a plugin."""
        plugin = Identifier(plugin).lower()
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.namespace == namespace)\
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

    def delete_plugin_value(self, plugin, key, namespace='default'):
        """Deletes the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.namespace == namespace)\
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

    def adjust_plugin_value(self, plugin, key, value, namespace='default'):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        value = json.dumps(value, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.namespace == namespace)\
                .filter(PluginValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
            if result:
                result.value = float(result.value) + float(value)
                session.commit()
            # DNE - Insert
            else:
                new_pluginvalue = PluginValues(plugin=plugin, namespace=namespace, key=key, value=float(value))
                session.add(new_pluginvalue)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def adjust_plugin_list(self, plugin, key, entries, adjustmentdirection, namespace='default'):
        """Sets the value for a given key to be associated with the plugin."""
        plugin = Identifier(plugin).lower()
        if not isinstance(entries, list):
            entries = [entries]
        entries = json.dumps(entries, ensure_ascii=False)
        session = self.ssession()
        try:
            result = session.query(PluginValues) \
                .filter(PluginValues.plugin == plugin)\
                .filter(PluginValues.namespace == namespace)\
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
                new_pluginvalue = PluginValues(plugin=plugin, namespace=namespace, key=key, value=values)
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

        sopel.db.NickIDs = NickIDs
        sopel.db.Nicknames = Nicknames
        sopel.db.NickValues = NickValues
        SopelDB.get_nick_value = SpiceDB.get_nick_value
        SopelDB.set_nick_value = SpiceDB.set_nick_value
        SopelDB.delete_nick_value = SpiceDB.delete_nick_value
        SopelDB.adjust_nick_value = SpiceDB.adjust_nick_value
        SopelDB.adjust_nick_list = SpiceDB.adjust_nick_list

        sopel.db.ChannelValues = ChannelValues
        SopelDB.get_channel_value = SpiceDB.get_channel_value
        SopelDB.set_channel_value = SpiceDB.set_channel_value
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
        BASE.metadata.create_all(self.db.engine)

    """Nick"""

    def get_nick_id(self, nick, create=True):
        return self.db.get_nick_id(nick, create)

    def alias_nick(self, nick, alias):
        return self.alias_nick(nick, alias)

    def check_nick_id(self, nick):
        try:
            self.db.get_nick_id(nick, create=False)
            return True
        except ValueError:
            return False

    def get_nick_value(self, nick, key, namespace='default'):
        return self.db.get_nick_value(nick, key, namespace)

    def set_nick_value(self, nick, key, value, namespace='default'):
        return self.db.set_nick_value(nick, key, value, namespace)

    def delete_nick_value(self, nick, key, namespace='default'):
        return self.db.delete_nick_value(nick, key, namespace)

    def adjust_nick_value(self, nick, key, value, namespace='default'):
        return self.db.adjust_nick_value(nick, key, value, namespace)

    def adjust_nick_list(self, nick, key, entries, adjustmentdirection, namespace='default'):
        return self.db.adjust_nick_list(nick, key, entries, adjustmentdirection, namespace)

    """Bot"""

    def get_bot_value(self, key, namespace='default'):
        return self.db.get_nick_value(botconfig.nick, key, namespace)

    def set_bot_value(self, key, value, namespace='default'):
        return self.db.set_nick_value(botconfig.nick, key, value, namespace)

    def delete_bot_value(self, key, namespace='default'):
        return self.db.delete_nick_value(botconfig.nick, key, namespace)

    def adjust_bot_value(self, key, value, namespace='default'):
        return self.db.adjust_nick_value(botconfig.nick, key, value, namespace)

    def adjust_bot_list(self, key, entries, adjustmentdirection, namespace='default'):
        return self.db.adjust_nick_list(botconfig.nick, key, entries, adjustmentdirection, namespace)

    """Channels"""

    def get_channel_value(self, channel, key, namespace='default'):
        return self.db.get_channel_value(channel, key, namespace)

    def set_channel_value(self, channel, key, value, namespace='default'):
        return self.db.set_channel_value(channel, key, value, namespace)

    def delete_channel_value(self, channel, key, namespace='default'):
        return self.db.delete_channel_value(channel, key, namespace)

    def adjust_channel_value(self, channel, key, value, namespace='default'):
        return self.db.adjust_channel_value(channel, key, value, namespace)

    def adjust_channel_list(self, nick, key, entries, adjustmentdirection, namespace='default'):
        return self.db.adjust_channel_list(nick, key, entries, adjustmentdirection, namespace)

    """Plugins"""

    def get_plugin_value(self, plugin, key, namespace='default'):
        return self.db.get_plugin_value(plugin, key, namespace)

    def set_plugin_value(self, plugin, key, value, namespace='default'):
        return self.db.set_plugin_value(plugin, key, value, namespace)

    def delete_plugin_value(self, plugin, key, namespace='default'):
        return self.db.delete_plugin_value(plugin, key, namespace)

    def adjust_plugin_value(self, plugin, key, value, namespace='default'):
        return self.db.adjust_plugin_value(plugin, key, value, namespace)

    def adjust_plugin_list(self, nick, key, entries, adjustmentdirection, namespace='default'):
        return self.db.adjust_plugin_list(nick, key, entries, adjustmentdirection, namespace)


db = BotDatabase()
