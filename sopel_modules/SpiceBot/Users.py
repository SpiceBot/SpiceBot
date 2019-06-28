# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to track users"""

from sopel.tools import Identifier

from .Database import db as botdb
from .Tools import is_number, inlist, similar, array_arrangesort

import spicemanip

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

    def ID(self, nickinput):
        if is_number(nickinput):
            nick_id = nickinput
            if nick_id in list(self.dict["current"].keys()):
                nick = self.dict["current"][nick_id]["nick"]
            elif nick_id in list(self.dict["all"].keys()) and len(self.dict["all"][nick_id]):
                nick = self.dict["all"][nick_id][0]
            else:
                raise Exception('ID ' + str(nickinput) + ' does not appear to be associated with a nick')
            return nick
        else:
            nick_id = self.whois_ident(nickinput)
            return nick_id

    def whois_ident(self, nick, usercreate=True):
        nick = Identifier(nick)
        try:
            nick_id = botdb.db.get_nick_id(nick, create=usercreate)
        except Exception as e:
            nick_id = e
            nick_id = None
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
                if str(channel).lower() not in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].append(str(channel).lower())
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
                if str(trigger.sender).lower() not in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].append(str(trigger.sender).lower())
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
        if str(trigger.sender).lower() not in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].append(str(trigger.sender).lower())
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
        if str(trigger.sender).lower() in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].remove(str(trigger.sender).lower())
        self.dict["current"][nick_id]["channels"] = []
        # mark user as offline
        if nick_id in self.dict["online"]:
            self.dict["online"].remove(nick_id)
        if nick_id not in self.dict["offline"]:
            self.dict["offline"].append(int(nick_id))

    def part(self, bot, trigger):
        if trigger.nick == bot.nick:
            for nick_id in list(self.dict["current"].keys()):
                if str(trigger.sender).lower() in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].remove(str(trigger.sender).lower())
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
        if str(trigger.sender).lower() in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].remove(str(trigger.sender).lower())
        # mark offline
        if not len(self.dict["current"][nick_id]["channels"]) and nick_id in self.dict["online"]:
            self.dict["online"].remove(nick_id)
        if not len(self.dict["current"][nick_id]["channels"]) and nick_id not in self.dict["offline"]:
            self.dict["offline"].append(int(nick_id))

    def kick(self, bot, trigger):
        targetnick = Identifier(str(trigger.args[1]))
        if targetnick == bot.nick:
            for nick_id in list(self.dict["current"].keys()):
                if str(trigger.sender).lower() in self.dict["current"][nick_id]["channels"]:
                    self.dict["current"][nick_id]["channels"].remove(str(trigger.sender).lower())
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
        if str(trigger.sender).lower() in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].remove(str(trigger.sender).lower())
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
        if str(trigger.sender).lower() not in self.dict["current"][nick_id]["channels"]:
            self.dict["current"][nick_id]["channels"].append(str(trigger.sender).lower())
        # mark user as online
        if nick_id not in self.dict["online"]:
            self.dict["online"].append(int(nick_id))
        if nick_id in self.dict["offline"]:
            self.dict["offline"].remove(nick_id)

    def mode(self, bot, trigger):
        return

    def targetcheck(self, posstarget):
        return True

        # idk whois
        if not botdb.check_nick_id(posstarget):
            return

    def nick_actual(self, nick, altlist=None):
        nick_id = self.whois_ident(nick)
        nick_actual = self.ID(nick_id)
        return nick_actual

    def target_online(self, nick, nick_id=None):
        if not nick_id:
            nick_id = self.ID(nick)
        if nick_id in self.dict["online"]:
            return True
        else:
            return False

    def target_check(self, bot, trigger, target, targetbypass):
        targetgood = {"targetgood": True, "error": "None", "reason": None}

        if not isinstance(targetbypass, list):
            targetbypass = [targetbypass]

        if "notarget" not in targetbypass:
            if not target or target == '':
                return {"targetgood": False, "error": "No target Given.", "reason": "notarget"}

        # Optional don't allow self-target
        if "self" not in targetbypass:
            if inlist(target, trigger.nick):
                return {"targetgood": False, "error": "This command does not allow you to target yourself.", "reason": "self"}

        # cannot target bots
        if "bot" not in targetbypass:
            if inlist(target, bot.nick):
                return {"targetgood": False, "error": "I am a bot and cannot be targeted.", "reason": "bot"}
        if "bots" not in targetbypass:
            if inlist(target, bot.nick):
                return {"targetgood": False, "error": self.nick_actual(bot, target) + " is a bot and cannot be targeted.", "reason": "bots"}

        nick_id = self.whois_ident(target, usercreate=False)

        # Not a valid user
        if "unknown" not in targetbypass:
            if not nick_id:
                sim_user, sim_num = [], []
                for nick_id in list(self.dict["all"].keys()):
                    nick_list = self.dict["all"][nick_id]
                    for nick in nick_list:
                        similarlevel = similar(str(target).lower(), nick.lower())
                        if similarlevel >= .75:
                            sim_user.append(nick)
                            sim_num.append(similarlevel)
                if sim_user != [] and sim_num != []:
                    sim_num, sim_user = array_arrangesort(bot, sim_num, sim_user)
                    closestmatch = spicemanip.main(sim_user, 'reverse', "list")
                    listnumb, relist = 1, []
                    for item in closestmatch:
                        if listnumb <= 3:
                            relist.append(str(item))
                        listnumb += 1
                    closestmatches = spicemanip.main(relist, "andlist")
                    targetgooderror = "It looks like you're trying to target someone! Did you mean: " + str(closestmatches) + "?"
                else:
                    targetgooderror = "I am not sure who that is."
                return {"targetgood": False, "error": targetgooderror, "reason": "unknown"}

        # User offline
        if "offline" not in targetbypass:
            if not self.target_online(target, nick_id):
                return {"targetgood": False, "error": "It looks like " + self.nick_actual(bot, target) + " is offline right now!", "reason": "offline"}

        # Private Message
        if "privmsg" not in targetbypass:
            if trigger.is_privmsg and not inlist(target, trigger.nick):
                return {"targetgood": False, "error": "Leave " + self.nick_actual(bot, target) + " out of this private conversation!", "reason": "privmsg"}

        # not in the same channel
        if "diffchannel" not in targetbypass:
            if not trigger.is_privmsg and self.target_online(target, nick_id):
                if str(trigger.sender).lower() not in self.dict["current"][nick_id]["channels"]:
                    return {"targetgood": False, "error": "It looks like " + self.nick_actual(bot, target) + " is online right now, but in a different channel.", "reason": "diffchannel"}

        return targetgood

    def random_valid_target(self, bot, trigger, outputtype):
        validtargs = []
        if trigger.is_privmsg:
            validtargs.extend([str(bot.nick), trigger.nick])
        else:
            for nick_id in self.dict["online"]:
                if str(trigger.sender).lower() in self.dict["current"][nick_id]["channels"]:
                    nick = self.dict["all"][nick_id][0]
                    validtargs.append(nick)
        if outputtype == 'list':
            return validtargs
        elif outputtype == 'random':
            return spicemanip.main(validtargs, 'random')


users = BotUsers()
