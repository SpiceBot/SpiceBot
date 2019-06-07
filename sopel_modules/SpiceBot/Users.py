# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to track users"""

from sopel.tools import Identifier

from .Database import db as botdb
from .Tools import inlist, inlist_match


class BotUsers():

    def __init__(self):
        self.all = botdb.get_bot_value('users') or []
        self.online = []
        self.save_user_db()

    def whois(self, nick):
        nick = Identifier(nick)
        nick_id = botdb.db.get_nick_id(nick, create=True)
        return nick_id

    def save_user_db(self):
        botdb.set_bot_value('users', self.all)

    def join(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            return
        # Identify
        nick_id = self.whois(trigger.nick)
        # mark online
        self.mark_online(trigger.nick, nick_id)

    def quit(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            return
        # Identify
        nick_id = self.whois(trigger.nick)
        # mark offline
        self.mark_offline(trigger.nick, nick_id)

    def part(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            return
        # Identify
        nick_id = self.whois(trigger.nick)
        # mark offline
        if trigger.nick not in bot.users:
            self.mark_offline(trigger.nick, nick_id)

    def kick(self, bot, trigger):
        target = str(trigger.args[1])
        # bot block
        if target == bot.nick:
            return
        # Identify
        nick_id = self.whois(target)
        # mark offline
        if target not in bot.users:
            self.mark_offline(target, nick_id)

    def add_to_all(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.whois(nick)
        # add to all if not there
        if nick_id not in self.all.keys():
            self.all[nick_id] = {"aliases": []}
        # add nick alias
        if nick not in self.all[nick_id]:
            self.all[nick_id]["aliases"].append(nick)

    def mark_online(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.whois(nick)
        self.add_to_all(nick, nick_id)
        if nick_id not in self.online:
            self.online.append(nick_id)

    def mark_offline(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.whois(nick)
        self.add_to_all(nick, nick_id)
        if nick_id in self.online:
            self.online.remove(nick_id)

    def current(self, bot, reqchannel='all'):
        user_list = []
        if reqchannel == 'all':
            for channel in bot.channels.keys():
                for user in bot.channels[channel].privileges.keys():
                    user_id = self.whois(user)
                    user_list.append(user_id)
            return user_list
        elif not inlist(reqchannel, bot.channels.keys()):
            return user_list
        else:
            channel = inlist_match(reqchannel, bot.channels.keys())
            for user in bot.channels[channel].privileges.keys():
                user_id = self.whois(user)
                user_list.append(user_id)
            return user_list


users = BotUsers()
