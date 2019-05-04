#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module


def configure(config):
    pass


def setup(bot):
    pass


def shutdown(bot):
    pass


"""Dyanmic Table Creation"""


def db_create_table(bot, tablename):
    bot.db._create_table(tablename)


"""Database Direct"""


# Get a value
def db_get_nick_value(bot, nick, key):
    database_value = bot.db.get_nick_value(nick, key) or None
    return database_value


# set a value
def db_set_nick_value(bot, nick, key, value):
    bot.db.set_nick_value(nick, key, value)


# DELETE a value
def db_reset_value(bot, nick, key):
    bot.db.reset_nick_value(nick, key)


# add or subtract from current value
def db_adjust_value(bot, nick, key, value):
    bot.db.adjust_nick_value(nick, key, value)


# list stored in database, add or remove elements
def db_adjust_list(bot, nick, entries, key, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    adjustlist = db_get_nick_value(bot, nick, key) or []
    adjustlistnew = []
    for x in adjustlist:
        adjustlistnew.append(x)
    db_reset_value(bot, nick, key)
    adjustlist = []
    if adjustmentdirection == 'add':
        for y in entries:
            if y not in adjustlistnew:
                adjustlistnew.append(y)
    elif adjustmentdirection == 'del':
        for y in entries:
            if y in adjustlistnew:
                adjustlistnew.remove(y)
    for x in adjustlistnew:
        if x not in adjustlist:
            adjustlist.append(x)
    if adjustlist == []:
        db_reset_value(bot, nick, key)
    else:
        db_set_nick_value(bot, nick, key, adjustlist)
