#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.tools import stderr, Identifier
from sopel.db import _deserialize, SopelDB

import json


def setup(bot):
    # Inject Database Functions
    stderr("[SpiceBot_Databaseaddons] Implanting Database functions into bot.")
    SopelDB.reset_nick_value = SopelDBCache.reset_nick_value
    SopelDB.adjust_nick_value = SopelDBCache.adjust_nick_value
    SopelDB.reset_channel_value = SopelDBCache.reset_channel_value
    SopelDB.adjust_channel_value = SopelDBCache.adjust_channel_value
    SopelDB._create_table = SopelDBCache._create_table


class SopelDBCache:

    """Dynamic Table Creation"""

    def _create_table(self, tablename):
        self.execute('CREATE TABLE IF NOT EXISTS ? (mainid STRING, key STRING, value STRING, PRIMARY KEY (mainid, key))', tablename)

    """Nicks"""

    def reset_nick_value(self, nick, key):
        """Resets the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        nick_id = self.get_nick_id(nick)
        self.execute('DELETE FROM nick_values WHERE nick_id = ? AND key = ?', [nick_id, key])

    def adjust_nick_value(self, nick, key, value):
        """Adjusts the value for a given key to be associated with the nick."""
        nick = Identifier(nick)
        result = self.execute(
            'SELECT value FROM nicknames JOIN nick_values '
            'ON nicknames.nick_id = nick_values.nick_id '
            'WHERE slug = ? AND key = ?',
            [nick.lower(), key]
        ).fetchone()
        if result is not None:
            result = result[0]
        current_value = _deserialize(result)
        value = current_value + value
        value = json.dumps(value, ensure_ascii=False)
        nick_id = self.get_nick_id(nick)
        self.execute('INSERT OR REPLACE INTO nick_values VALUES (?, ?, ?)',
                     [nick_id, key, value])

    """Channels"""

    def reset_channel_value(self, channel, key):
        """Resets the value for a given key to be associated with a channel."""
        channel = Identifier(channel).lower()
        self.execute('DELETE FROM channel_values WHERE channel = ? AND key = ?', [channel, key])

    def adjust_channel_value(self, channel, key, value):
        """Adjusts the value for a given key to be associated with the channel."""
        channel = Identifier(channel).lower()
        result = self.execute(
            'SELECT value FROM channel_values WHERE channel = ? AND key = ?',
            [channel, key]
        ).fetchone()
        if result is not None:
            result = result[0]
        current_value = _deserialize(result)
        value = current_value + value
        value = json.dumps(value, ensure_ascii=False)
        self.execute('INSERT OR REPLACE INTO channel_values VALUES (?, ?, ?)',
                     [channel, key, value])
