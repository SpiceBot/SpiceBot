#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.tools import Identifier
from sopel_modules.SpiceBot_SBTools import bot_logging
from sopel.db import SopelDB, NickValues, ChannelValues
from sqlalchemy.exc import SQLAlchemyError

import json


def setup(bot):
    pass
    # Inject Database Functions
    bot_logging(bot, 'SpiceBot_Databaseaddons', "Implanting Database functions into bot")
    SopelDB.delete_nick_value = SopelDBCache.delete_nick_value
    SopelDB.adjust_nick_value = SopelDBCache.adjust_nick_value
    SopelDB.delete_channel_value = SopelDBCache.delete_channel_value
    SopelDB.adjust_channel_value = SopelDBCache.adjust_channel_value


class SopelDBCache:

    """Nicks"""

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

    """Channels"""

    def delete_channel_value(self, channel, key):
        """Sets the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        session = self.ssession()
        try:
            result = session.query(ChannelValues) \
                .filter(ChannelValues.channel == channel)\
                .filter(ChannelValues.key == key) \
                .one_or_none()
            # ChannelValue exists, update
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
