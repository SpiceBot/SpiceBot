# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to track users"""

from sopel.tools import Identifier

from .Database import db as botdb


class BotUsers():

    def __init__(self):
        # TODO timestamp for new .seen
        self.all = botdb.get_bot_value('users') or dict()
        self.online = []
        self.offline = []
        for user_id in self.all.keys():
            self.offline.append(user_id)
        self.current = {}

    def whois(self, nick):
        nick_id = self.whois_id(nick)
        self.add_to_all(nick, nick_id)
        self.add_to_current(nick, nick_id)
        return self.current[nick_id]["nick"]

    def whois_id(self, nick):
        nick = Identifier(nick)
        nick_id = botdb.db.get_nick_id(nick, create=True)
        return nick_id

    def save_user_db(self):
        botdb.set_bot_value('users', self.all)

    def add_to_all(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.whois_id(nick)
        # add to all if not there
        if nick_id not in self.all.keys():
            self.all[nick_id] = []
        # add nick alias
        if nick not in self.all[nick_id]:
            self.all[nick_id].append(nick)
        self.save_user_db()

    def add_to_current(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.whois_id(nick)
        # add to current if not there
        if nick_id not in self.current.keys():
            self.current[nick_id] = {"channels": [], "nick": nick}

    def join(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            for user in bot.channels[trigger.sender].privileges.keys():
                # Identify
                nick_id = self.whois_id(user)
                # Verify nick is in the all list
                self.add_to_all(user, nick_id)
                # Verify nick is in the all list
                self.add_to_current(user, nick_id)
                # set current nick
                self.current[nick_id]["nick"] = user
                # add joined channel to nick list
                if trigger.sender not in self.current[nick_id]["channels"]:
                    self.current[nick_id]["channels"].append(trigger.sender)
                # mark user as online
                if nick_id not in self.online:
                    self.online.append(nick_id)
                if nick_id in self.offline:
                    self.offline.remove(nick_id)
            return
        # Identify
        nick_id = self.whois_id(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # set current nick
        self.current[nick_id]["nick"] = trigger.nick
        # add joined channel to nick list
        if trigger.sender not in self.current[nick_id]["channels"]:
            self.current[nick_id]["channels"].append(trigger.sender)
        # mark user as online
        if nick_id not in self.online:
            self.online.append(nick_id)
        if nick_id in self.offline:
            self.offline.remove(nick_id)

    def quit(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            return
        # Identify
        nick_id = self.whois_id(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # empty nicks channel list
        if trigger.sender in self.current[nick_id]["channels"]:
            self.current[nick_id]["channels"].remove(trigger.sender)
        self.current[nick_id]["channels"] = []
        # mark user as offline
        if nick_id in self.online:
            self.online.remove(nick_id)
        if nick_id not in self.offline:
            self.offline.append(nick_id)

    def part(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            for nick_id in self.current.keys():
                if trigger.sender in self.current[nick_id]["channels"]:
                    self.current[nick_id]["channels"].remove(trigger.sender)
                # mark offline
                if not len(self.current[nick_id]["channels"]) and nick_id in self.online:
                    self.online.remove(nick_id)
                if not len(self.current[nick_id]["channels"]) and nick_id not in self.offline:
                    self.offline.append(nick_id)
            return
        # Identify
        nick_id = self.whois_id(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # remove channel from nick list
        if trigger.sender in self.current[nick_id]["channels"]:
            self.current[nick_id]["channels"].remove(trigger.sender)
        # mark offline
        if not len(self.current[nick_id]["channels"]) and nick_id in self.online:
            self.online.remove(nick_id)
        if not len(self.current[nick_id]["channels"]) and nick_id not in self.offline:
            self.offline.append(nick_id)

    def kick(self, bot, trigger):
        targetnick = Identifier(str(trigger.args[1]))
        # bot block
        if targetnick == bot.nick:
            for nick_id in self.current.keys():
                if trigger.sender in self.current[nick_id]["channels"]:
                    self.current[nick_id]["channels"].remove(trigger.sender)
                # mark offline
                if not len(self.current[nick_id]["channels"]) and nick_id in self.online:
                    self.online.remove(nick_id)
                if not len(self.current[nick_id]["channels"]) and nick_id not in self.offline:
                    self.offline.append(nick_id)
            return
        # Identify
        nick_id = self.whois_id(targetnick)
        # Verify nick is in the all list
        self.add_to_all(targetnick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(targetnick, nick_id)
        # remove channel from nick list
        if trigger.sender in self.current[nick_id]["channels"]:
            self.current[nick_id]["channels"].remove(trigger.sender)
        # mark offline
        if not len(self.current[nick_id]["channels"]) and nick_id in self.online:
            self.online.remove(nick_id)
        if not len(self.current[nick_id]["channels"]) and nick_id not in self.offline:
            self.offline.append(nick_id)

    def nick(self, bot, trigger):
        newnick = Identifier(trigger)
        # bot block
        if trigger.nick == bot.nick or newnick == bot.nick:
            return
        # alias the nick
        if not botdb.check_nick_id(newnick):
            botdb.alias_nick(trigger.nick, newnick)
        # Identify
        nick_id = self.whois_id(newnick)
        # Verify nick is in the all list
        self.add_to_all(newnick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(newnick, nick_id)
        # set current nick
        self.current[nick_id]["nick"] = newnick
        # add joined channel to nick list
        if trigger.sender not in self.current[nick_id]["channels"]:
            self.current[nick_id]["channels"].append(trigger.sender)
        # mark user as online
        if nick_id not in self.online:
            self.online.append(nick_id)
        if nick_id in self.offline:
            self.offline.remove(nick_id)

    def mode(self, bot, trigger):
        return


users = BotUsers()
