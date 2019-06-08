# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to track users"""

from sopel.tools import Identifier

from .Database import db as botdb
from .Tools import is_number

# TODO timestamp for new .seen


class BotUsers():

    def __init__(self):
        self.dict = {
                    "all": botdb.get_bot_value('users') or {},
                    "online": [],
                    "offline": [],
                    "current": {},
                    }
        """during setup, all users from database are offline until marked online"""
        for user_id in list(self.dict["all"].keys()):
            self.dict["offline"].append(int(user_id))

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        """We will try to find a dict value, or return None"""
        if name.lower() in list(self.dict.keys()):
            return self.dict[str(name).lower()]
        else:
            raise Exception('User dict does not contain a function or key ' + str(name.lower()))

    def ID(self, nick):
        if is_number(nick):
            if nick in list(self.dict["current"].keys()):
                return self.dict["current"][nick]["nick"]
            elif nick in list(self.dict["all"].keys()) and len(self.dict["all"][nick]):
                return self.dict["all"][nick][0]
            else:
                raise Exception('ID ' + str(nick) + ' does not appear to be associated with a nick')
        else:
            nick_id = self.whois_ident(nick)
            return nick_id

    def whois_ident(self, nick):
        nick = Identifier(nick)
        nick_id = botdb.db.get_nick_id(nick, create=True)
        return int(nick_id)

    def save_user_db(self):
        botdb.set_bot_value('users', self.dict["all"])

    def add_to_all(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.ID(nick)
        # add to all if not there
        if nick_id not in list(self.dict["all"].keys()):
            self.dict["all"][nick_id] = []
        # add nick alias as index 0
        if nick in self.dict["all"][nick_id]:
            self.dict["all"][nick_id].remove(nick)
        self.dict["all"][nick_id].insert(0, nick)
        self.save_user_db()

    def add_to_current(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.whois_ident(nick)
        # add to current if not there
        if nick_id not in list(self.dict["current"].keys()):
            self.dict["current"][nick_id] = {"channels": [], "nick": nick}

    def channel_scan(self, bot):
        for channel in list(bot.channels.keys()):
            for user in list(bot.channels[channel].privileges.keys()):
                # Identify
                nick_id = self.whois_ident(user)
                # Verify nick is in the all list
                self.add_to_all(user, nick_id)
                # Verify nick is in the all list
                self.add_to_current(user, nick_id)
                # set current nick
                self.dict["current"][nick_id]["nick"] = user
                # add joined channel to nick list
                if channel not in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].append(channel)
                # mark user as online
                if nick_id not in self.dict["online"]:
                    self.dict["online"].append(int(nick_id))
                if nick_id in self.dict["offline"]:
                    self.dict["offline"].remove(nick_id)

    def join(self, bot, trigger):
        if trigger.nick == bot.nick:
            for user in list(bot.channels[trigger.sender].privileges.keys()):
                # Identify
                nick_id = self.whois_ident(user)
                # Verify nick is in the all list
                self.add_to_all(user, nick_id)
                # Verify nick is in the all list
                self.add_to_current(user, nick_id)
                # set current nick
                self.dict["current"][nick_id]["nick"] = user
                # add joined channel to nick list
                if trigger.sender not in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].append(trigger.sender)
                # mark user as online
                if nick_id not in self.dict["online"]:
                    self.dict["online"].append(int(nick_id))
                if nick_id in self.dict["offline"]:
                    self.dict["offline"].remove(nick_id)
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # set current nick
        self.dict["current"][nick_id]["nick"] = trigger.nick
        # add joined channel to nick list
        if trigger.sender not in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].append(trigger.sender)
        # mark user as online
        if nick_id not in self.dict["online"]:
            self.dict["online"].append(int(nick_id))
        if nick_id in self.dict["offline"]:
            self.dict["offline"].remove(nick_id)

    def quit(self, bot, trigger):
        if trigger.nick == bot.nick:
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # empty nicks channel list
        if trigger.sender in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].remove(trigger.sender)
        self.dict["current"][nick_id]["channels"] = []
        # mark user as offline
        if nick_id in self.dict["online"]:
            self.dict["online"].remove(nick_id)
        if nick_id not in self.dict["offline"]:
            self.dict["offline"].append(int(nick_id))

    def part(self, bot, trigger):
        if trigger.nick == bot.nick:
            for nick_id in list(self.dict["current"].keys()):
                if trigger.sender in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].remove(trigger.sender)
                # mark offline
                if not len(self.dict["current"][nick_id]["channels"]) and nick_id in self.dict["online"]:
                    self.dict["online"].remove(nick_id)
                if not len(self.dict["current"][nick_id]["channels"]) and nick_id not in self.dict["offline"]:
                    self.dict["offline"].append(int(nick_id))
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # remove channel from nick list
        if trigger.sender in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].remove(trigger.sender)
        # mark offline
        if not len(self.dict["current"][nick_id]["channels"]) and nick_id in self.dict["online"]:
            self.dict["online"].remove(nick_id)
        if not len(self.dict["current"][nick_id]["channels"]) and nick_id not in self.dict["offline"]:
            self.dict["offline"].append(int(nick_id))

    def kick(self, bot, trigger):
        targetnick = Identifier(str(trigger.args[1]))
        if targetnick == bot.nick:
            for nick_id in list(self.dict["current"].keys()):
                if trigger.sender in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].remove(trigger.sender)
                # mark offline
                if not len(self.dict["current"][nick_id]["channels"]) and nick_id in self.dict["online"]:
                    self.dict["online"].remove(nick_id)
                if not len(self.dict["current"][nick_id]["channels"]) and nick_id not in self.dict["offline"]:
                    self.dict["offline"].append(int(nick_id))
            return
        # Identify
        nick_id = self.whois_ident(targetnick)
        # Verify nick is in the all list
        self.add_to_all(targetnick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(targetnick, nick_id)
        # remove channel from nick list
        if trigger.sender in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].remove(trigger.sender)
        # mark offline
        if not len(self.dict["current"][nick_id]["channels"]) and nick_id in self.dict["online"]:
            self.dict["online"].remove(nick_id)
        if not len(self.dict["current"][nick_id]["channels"]) and nick_id not in self.dict["offline"]:
            self.dict["offline"].append(int(nick_id))

    def nick(self, bot, trigger):
        newnick = Identifier(trigger)
        if trigger.nick == bot.nick or newnick == bot.nick:
            return
        # alias the nick
        if not botdb.check_nick_id(newnick):
            botdb.alias_nick(trigger.nick, newnick)
        # Identify
        nick_id = self.whois_ident(newnick)
        # Verify nick is in the all list
        self.add_to_all(newnick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(newnick, nick_id)
        # set current nick
        self.dict["current"][nick_id]["nick"] = newnick
        # add joined channel to nick list
        if trigger.sender not in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].append(trigger.sender)
        # mark user as online
        if nick_id not in self.dict["online"]:
            self.dict["online"].append(int(nick_id))
        if nick_id in self.dict["offline"]:
            self.dict["offline"].remove(nick_id)

    def mode(self, bot, trigger):
        return


users = BotUsers()
