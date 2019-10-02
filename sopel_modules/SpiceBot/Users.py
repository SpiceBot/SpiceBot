# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to track users"""

import sopel
from sopel.tools import Identifier

from .Database import db as botdb
from .Tools import is_number, inlist, similar, array_arrangesort, bot_privs, channel_privs

from sopel_modules.spicemanip import spicemanip

import threading
import re
import time

# TODO timestamp for new .seen


class BotUsers():

    def __init__(self):
        self.who_reqs = {}
        self.lock = threading.Lock()
        # TODO AWAY
        self.dict = {
                    "all": botdb.get_bot_value('users') or {},
                    "online": [],
                    "offline": [],
                    "away": [],
                    "current": {},
                    "registered": botdb.get_bot_value('regged_users') or [],
                    "register_check": {},
                    "identified": [],
                    }
        """during setup, all users from database are offline until marked online"""
        # for user_id in list(self.dict["all"].keys()):
        #    self.mark_user_offline(user_id)
        self.lock.acquire()
        self.dict["offline"] = list(self.dict["all"].keys())
        self.lock.release()

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
            self.lock.acquire()
            if int(nick_id) in list(self.dict["current"].keys()):
                nick = self.dict["current"][int(nick_id)]["nick"]
                self.lock.release()
            elif int(nick_id) in list(self.dict["all"].keys()) and len(self.dict["all"][int(nick_id)]):
                nick = self.dict["all"][int(nick_id)][0]
                self.lock.release()
            else:
                raise Exception('ID ' + str(nickinput) + ' does not appear to be associated with a nick')
            return nick
        else:
            nick_id = self.whois_ident(nickinput)
            return int(nick_id)

    def whois_ident(self, nick, usercreate=True):
        nick = Identifier(nick)
        try:
            nick_id = botdb.db.get_nick_id(nick, create=usercreate)
        except Exception as e:
            nick_id = e
            nick_id = None
            return None
        if usercreate and nick_id:
            self.add_to_all(nick, nick_id)
        return int(nick_id)

    def save_user_db(self):
        botdb.set_bot_value('users', self.dict["all"])
        botdb.set_bot_value('regged_users', self.dict["registered"])

    def add_to_all(self, nick, nick_id=None):
        self.lock.acquire()
        if not nick_id:
            nick_id = self.ID(nick)
        # add to all if not there
        if int(nick_id) not in list(self.dict["all"].keys()):
            self.dict["all"][int(nick_id)] = []
        # add nick alias as index 0
        if nick in self.dict["all"][int(nick_id)]:
            self.dict["all"][int(nick_id)].remove(nick)
        self.dict["all"][int(nick_id)].insert(0, nick)
        self.lock.release()
        self.save_user_db()

    def add_to_current(self, nick, nick_id=None):
        self.lock.acquire()
        if not nick_id:
            nick_id = self.whois_ident(nick)
        # add to current if not there
        if int(nick_id) not in list(self.dict["current"].keys()):
            self.dict["current"][int(nick_id)] = {"channels": [], "nick": nick}
        self.lock.release()

    def channel_scan(self, bot):
        for channel in list(bot.channels.keys()):
            for user in list(bot.channels[channel].privileges.keys()):
                # Identify
                nick_id = self.whois_ident(user)
                # check if nick is registered
                self.whois_send(bot, user)
                # Verify nick is in the all list
                self.add_to_all(user, nick_id)
                # Verify nick is in the all list
                self.add_to_current(user, nick_id)
                # set current nick
                self.mark_current_nick(user, nick_id)
                # add joined channel to nick list
                self.add_channel(channel, nick_id)
                # mark user as online
                self.mark_user_online(nick_id)

    def mark_current_nick(self, nick, nick_id):
        self.lock.acquire()
        self.dict["current"][int(nick_id)]["nick"] = nick
        self.lock.release()

    def add_channel(self, channel, nick_id):
        self.lock.acquire()
        if str(channel).lower() not in self.dict["current"][int(nick_id)]["channels"]:
            self.dict["current"][int(nick_id)]["channels"].append(str(channel).lower())
        self.lock.release()

    def remove_channel(self, channel, nick_id):
        self.lock.acquire()
        if str(channel).lower() in self.dict["current"][int(nick_id)]["channels"]:
            self.dict["current"][int(nick_id)]["channels"].remove(str(channel).lower())
        self.lock.release()

    def mark_user_online(self, nick_id):
        self.lock.acquire()
        if int(nick_id) not in self.dict["online"]:
            self.dict["online"].append(int(nick_id))
        if int(nick_id) in self.dict["offline"]:
            self.dict["offline"].remove(int(nick_id))
        self.lock.release()

    def mark_user_offline(self, nick_id):
        self.lock.acquire()
        if int(nick_id) in self.dict["online"]:
            self.dict["online"].remove(int(nick_id))
        if int(nick_id) not in self.dict["offline"]:
            self.dict["offline"].append(int(nick_id))
        self.lock.release()
        self.whois_identify_forget(nick_id)

    def join(self, bot, trigger):
        if trigger.nick == bot.nick:
            for user in list(bot.channels[trigger.sender].privileges.keys()):
                # Identify
                nick_id = self.whois_ident(user)
                # check if nick is registered
                self.whois_send(bot, user)
                # Verify nick is in the all list
                self.add_to_all(user, nick_id)
                # Verify nick is in the all list
                self.add_to_current(user, nick_id)
                # set current nick
                self.mark_current_nick(user, nick_id)
                # add joined channel to nick list
                self.add_channel(trigger.sender, nick_id)
                # mark user as online
                self.mark_user_online(nick_id)
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # check if nick is registered
        self.whois_send(bot, trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # set current nick
        self.mark_current_nick(trigger.nick, nick_id)
        # add joined channel to nick list
        self.add_channel(trigger.sender, nick_id)
        # mark user as online
        self.mark_user_online(nick_id)

    def chat(self, bot, trigger):
        if trigger.nick == bot.nick:
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # check if nick is registered
        self.whois_send(bot, trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # set current nick
        self.mark_current_nick(trigger.nick, nick_id)
        # add joined channel to nick list
        self.add_channel(trigger.sender, nick_id)
        # mark user as online
        self.mark_user_online(nick_id)

    def quit(self, bot, trigger):
        if trigger.nick == bot.nick:
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # check if nick is registered
        self.whois_send(bot, trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # empty nicks channel list
        self.remove_channel(trigger.sender, nick_id)
        # mark user as offline
        self.mark_user_offline(nick_id)

    def part(self, bot, trigger):
        if trigger.nick == bot.nick:
            for nick_id in list(self.dict["current"].keys()):
                self.remove_channel(trigger.sender, nick_id)
                # mark offline
                self.mark_user_offline(nick_id)
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # check if nick is registered
        self.whois_send(bot, trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # remove channel from nick list
        self.remove_channel(trigger.sender, nick_id)
        # mark offline
        self.mark_user_offline(nick_id)

    def kick(self, bot, trigger):
        targetnick = Identifier(str(trigger.args[1]))
        if targetnick == bot.nick:
            for nick_id in list(self.dict["current"].keys()):
                self.remove_channel(trigger.sender, nick_id)
                # mark offline
                self.mark_user_offline(nick_id)
            return
        # Identify
        nick_id = self.whois_ident(targetnick)
        # check if nick is registered
        self.whois_send(bot, targetnick)
        # Verify nick is in the all list
        self.add_to_all(targetnick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(targetnick, nick_id)
        # remove channel from nick list
        self.remove_channel(trigger.sender, nick_id)
        # mark offline
        self.mark_user_offline(nick_id)

    def nick(self, bot, trigger):
        oldnick = trigger.nick
        old_nick_id = self.whois_ident(oldnick)
        self.whois_identify_forget(old_nick_id)
        newnick = Identifier(trigger)
        if oldnick == bot.nick or newnick == bot.nick:
            return
        # check if nick is registered
        self.whois_send(bot, newnick)
        # Verify nick is in the all list
        self.add_to_all(oldnick, old_nick_id)
        # Verify nick is in the all list
        self.add_to_current(oldnick, old_nick_id)
        # set current nick
        self.mark_current_nick(newnick, old_nick_id)
        # add joined channel to nick list
        self.add_channel(trigger.sender, old_nick_id)
        # mark user as online
        self.mark_user_online(old_nick_id)
        # alias the nick
        # try:
        #    botdb.alias_nick(oldnick, newnick)
        # except Exception as e:
        #    old_nick_id = e
        #    return

    def mode(self, bot, trigger):
        return

    def rpl_names(self, bot, trigger):
        """Handle NAMES response, happens when joining to channels."""
        names = trigger.split()

        # TODO specific to one channel type. See issue 281.
        channels = re.search(r'(#\S*)', trigger.raw)
        if not channels:
            return
        channel = Identifier(channels.group(1))

        mapping = {'+': sopel.module.VOICE,
                   '%': sopel.module.HALFOP,
                   '@': sopel.module.OP,
                   '&': sopel.module.ADMIN,
                   '~': sopel.module.OWNER}

        for name in names:
            nick = Identifier(name.lstrip(''.join(mapping.keys())))
            # Identify
            nick_id = self.whois_ident(nick)
            # Verify nick is in the all list
            self.add_to_all(nick, nick_id)
            # Verify nick is in the all list
            self.add_to_current(nick, nick_id)
            # set current nick
            self.mark_current_nick(nick, nick_id)
            # add joined channel to nick list
            self.add_channel(channel, nick_id)
            # mark user as online
            self.mark_user_online(nick_id)
            # check if nick is registered
            self.whois_send(bot, nick)

    def rpl_who(self, bot, trigger):
        if len(trigger.args) < 2 or trigger.args[1] not in self.who_reqs:
            # Ignored, some module probably called WHO
            return
        if len(trigger.args) != 8:
            return
        _, _, channel, user, host, nick, status, account = trigger.args
        nick = Identifier(nick)
        channel = Identifier(channel)
        # Identify
        nick_id = self.whois_ident(nick)
        # Verify nick is in the all list
        self.add_to_all(nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(nick, nick_id)
        # set current nick
        self.mark_current_nick(nick, nick_id)
        # add joined channel to nick list
        self.add_channel(channel, nick_id)
        # mark user as online
        self.mark_user_online(nick_id)
        # check if nick is registered
        self.whois_send(bot, nick)

    def rpl_whois(self, bot, trigger):
        if not bot.config.SpiceBot_regnick.regnick:
            return
        nick = trigger.args[1]
        self.whois_handle(nick)

    def whois_handle(self, nick):
        nick_id = self.whois_ident(nick)
        self.lock.acquire()
        # identified
        if int(nick_id) not in self.dict["identified"]:
            self.dict["identified"].append(int(nick_id))
        # registered
        if str(nick).lower() not in [x.lower() for x in self.dict["registered"]]:
            self.dict["registered"].append(str(nick))
        self.lock.release()

    def whois_send(self, bot, nick):
        if not bot.config.SpiceBot_regnick.regnick:
            return
        check_whois = False
        nick_id = self.whois_ident(nick)

        # No registered check
        if int(nick_id) not in list(self.dict["register_check"].keys()):
            check_whois = True
        elif int(nick_id) in self.dict["identified"]:
            timestamp = self.dict["register_check"][int(nick_id)]
            if time.time() - timestamp >= 1800:
                check_whois = True
        else:
            timestamp = self.dict["register_check"][int(nick_id)]
            if time.time() - timestamp >= 240:
                check_whois = True
        if check_whois:
            bot.write(['WHOIS', str(nick)])
            self.lock.acquire()
            self.dict["register_check"][int(nick_id)] = time.time()
            self.lock.release()

    def whois_identify_forget(self, nick_id):
        self.lock.acquire()
        if int(nick_id) in self.dict["identified"]:
            self.dict["identified"].remove(int(nick_id))
        if int(nick_id) in list(self.dict["register_check"].keys()):
            del self.dict["register_check"][int(nick_id)]
        self.lock.release()

    def account(self, bot, trigger):
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # set current nick
        self.mark_current_nick(trigger.nick, nick_id)
        # mark user as online
        self.mark_user_online(nick_id)

    def track_notify(self, bot, trigger):
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is in the all list
        self.add_to_all(trigger.nick, nick_id)
        # Verify nick is in the all list
        self.add_to_current(trigger.nick, nick_id)
        # set current nick
        self.mark_current_nick(trigger.nick, nick_id)
        # mark user as online
        self.mark_user_online(nick_id)

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
                return {"targetgood": False, "error": self.nick_actual(target) + " is a bot and cannot be targeted.", "reason": "bots"}

        # Not a valid user
        if "unknown" not in targetbypass:
            if not botdb.check_nick_id(target):
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
                    closestmatch = spicemanip(sim_user, 'reverse', "list")
                    listnumb, relist = 1, []
                    for item in closestmatch:
                        if listnumb <= 3:
                            relist.append(str(item))
                        listnumb += 1
                    closestmatches = spicemanip(relist, "andlist")
                    targetgooderror = "It looks like you're trying to target someone! Did you mean: " + str(closestmatches) + "?"
                else:
                    targetgooderror = "I am not sure who that is."
                return {"targetgood": False, "error": targetgooderror, "reason": "unknown"}

        nick_id = self.whois_ident(target, usercreate=False)

        # User offline
        if "offline" not in targetbypass:
            if not self.target_online(target, nick_id):
                return {"targetgood": False, "error": "It looks like " + self.nick_actual(target) + " is offline right now!", "reason": "offline"}

        # Private Message
        if "privmsg" not in targetbypass:
            if trigger.is_privmsg and not inlist(target, trigger.nick):
                return {"targetgood": False, "error": "Leave " + self.nick_actual(target) + " out of this private conversation!", "reason": "privmsg"}

        # not in the same channel
        if "diffchannel" not in targetbypass:
            if not trigger.is_privmsg and self.target_online(target, nick_id):
                if str(trigger.sender).lower() not in self.dict["current"][nick_id]["channels"]:
                    return {"targetgood": False, "error": "It looks like " + self.nick_actual(target) + " is online right now, but in a different channel.", "reason": "diffchannel"}

        # not a registered nick
        # TODO
        # if "unregged" not in targetbypass:
        #    if bot.config.SpiceBot_regnick.regnick:
        #        if str(target).lower() not in [x.lower() for x in self.dict["registered"]]:
        #            return {"targetgood": False, "error": "It looks like " + self.nick_actual(target) + " is not a registered nick.", "reason": "unregged"}
        # TODO identified

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
            return spicemanip(validtargs, 'random')

    def command_permissions_check(self, bot, trigger, privslist):

        nick_id = self.whois_ident(trigger.nick)
        if bot.config.SpiceBot_regnick.regnick:
            if int(nick_id) not in self.dict["identified"]:
                return False

        commandrunconsensus = []

        for botpriv in ["admins", "owner"]:
            if botpriv in privslist:
                botpriveval = bot_privs(botpriv)
                if not inlist(trigger.nick, botpriveval):
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')

        if not trigger.is_privmsg:
            for chanpriv in ['OP', 'HOP', 'VOICE', 'OWNER', 'ADMIN']:
                if chanpriv in privslist:
                    chanpriveval = channel_privs(bot, trigger.sender, chanpriv)
                    if not inlist(trigger.nick, chanpriveval):
                        commandrunconsensus.append('False')
                    else:
                        commandrunconsensus.append('True')

        if not len(privslist):
            commandrunconsensus.append('True')

        if 'True' not in commandrunconsensus:
            return False

        return True


users = BotUsers()
