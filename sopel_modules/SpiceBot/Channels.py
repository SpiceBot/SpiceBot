# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel
from sopel.tools import Identifier
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute

import re
import threading

from .Config import config as botconfig
from .Database import db as botdb
from .Users import users as botusers


class SpiceBot_Channels_MainSection(StaticSection):
    announcenew = ValidatedAttribute('announcenew', default=False)
    joinall = ValidatedAttribute('joinall', default=False)
    operadmin = ValidatedAttribute('operadmin', default=False)
    chanignore = ListAttribute('chanignore')


class BotChannels():
    """This Logs all channels known to the server"""
    def __init__(self):
        self.setup_channels()

        self.lock = threading.Lock()
        self.channel_lock = False
        self.channels = []
        self.dict = {
                    "list": {},
                    "InitialProcess": False
                    }

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        """We will try to find a dict value, or return None"""
        if name.lower() in list(self.dict.keys()):
            return self.dict[str(name).lower()]
        else:
            raise Exception('Channel dict does not contain a function or key ' + str(name.lower()))

    def get_channel_users(self, channel, idtype="nick"):

        if channel.lower() not in list(self.dict["list"].keys()):
            raise Exception('Channel ' + str(channel.lower()) + " does not seem to be on this server")
        if 'users' not in list(self.dict["list"][channel.lower()].keys()) or not self.check_channel_bot(channel):
            raise Exception('Channel ' + str(channel.lower()) + " does not seem to be a channel the bot is in")

        nick_ids = self.dict["list"][channel.lower()]['users']
        if idtype.upper() == "ID":
            return nick_ids
        else:
            nick_list = []
            for nick_id in nick_ids:
                nickname = botusers.ID(nick_id)
                nick_list.append(nickname)
        return nick_list

    def setup_channels(self):
        botconfig.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)

    def channel_list_request(self, bot):
        bot.write(['LIST'])

    def channel_list_recieve_start(self):
        self.channel_lock = True

    def channel_list_recieve_input(self, trigger):
        self.lock.acquire()
        channel, _, topic = trigger.args[1:]
        if channel.lower() not in list(self.dict['list'].keys()):
            self.dict['list'][channel.lower()] = dict()
        self.dict['list'][channel.lower()]['name'] = channel
        self.dict['list'][channel.lower()]['topic'] = self.topic_compile(topic)
        self.channel_lock = True
        self.lock.release()

    def channel_list_recieve_finish(self):
        self.lock.acquire()
        if not self.dict['InitialProcess']:
            self.dict['InitialProcess'] = True
        self.lock.release()
        self.channel_lock = False

    def topic_compile(self, topic):
        actual_topic = re.compile(r'^\[\+[a-zA-Z]+\] (.*)')
        topic = re.sub(actual_topic, r'\1', topic)
        return topic

    def bot_part_empty(self, bot):
        """Don't stay in empty channels"""
        ignorepartlist = []
        if bot.config.core.logging_channel:
            ignorepartlist.append(bot.config.core.logging_channel)
        for channel in list(bot.channels.keys()):
            if len(list(bot.channels[channel].privileges.keys())) == 1 and channel not in ignorepartlist and channel.startswith("#"):
                bot.part(channel, "Leaving Empty Channel")
                if channel.lower() in self.dict['list']:
                    self.lock.acquire()
                    del self.dict['list'][channel.lower()]
                    self.lock.release()
                if channel.lower() in self.channels:
                    self.channels.remove(channel.lower())

    def join_all_channels(self, bot):
        if botconfig.SpiceBot_Channels.joinall:
            for channel in list(self.dict['list'].keys()):
                if channel.startswith("#"):
                    if channel not in list(bot.channels.keys()) and channel not in botconfig.SpiceBot_Channels.chanignore:
                        bot.write(('JOIN', bot.nick, self.dict['list'][channel]['name']))
                        if channel not in list(bot.channels.keys()) and botconfig.SpiceBot_Channels.operadmin:
                            bot.write(('SAJOIN', bot.nick, self.dict['list'][channel]['name']))

                        if channel in list(bot.channels.keys()):
                            if channel.lower() not in self.channels:
                                self.channels.append(channel.lower())

    def chanadmin_all_channels(self, bot):
        # Chan ADMIN +a
        for channel in list(bot.channels.keys()):
            if channel.startswith("#"):
                if channel not in botconfig.SpiceBot_Channels.chanignore:
                    if botconfig.SpiceBot_Channels.operadmin:
                        if not bot.channels[channel].privileges[bot.nick] < sopel.module.ADMIN:
                            bot.write(('SAMODE', channel, "+a", bot.nick))
                else:
                    bot.part(channel)

                    if channel not in list(bot.channels.keys()):
                        if channel.lower() in self.channels:
                            self.channels.remove(channel.lower())

    def whois_ident(self, nick):
        nick = Identifier(nick)
        nick_id = botdb.db.get_nick_id(nick, create=True)
        return nick_id

    def add_to_channel(self, channel, nick, nick_id=None):
        channel = str(channel)
        if not nick_id:
            nick_id = self.whois_ident(nick)
        if channel.lower() not in list(self.dict['list'].keys()):
            self.dict['list'][channel.lower()] = dict()
        if 'users' not in self.dict['list'][channel.lower()]:
            self.dict['list'][channel.lower()]['users'] = []
        if nick_id not in self.dict['list'][channel.lower()]['users']:
            self.dict['list'][channel.lower()]['users'].append(int(nick_id))
        if channel.lower() not in self.channels:
            self.channels.append(channel.lower())

    def remove_from_channel(self, channel, nick, nick_id=None):
        channel = str(channel)
        if not nick_id:
            nick_id = self.whois_ident(nick)
        if channel.lower() not in list(self.dict['list'].keys()):
            self.dict['list'][channel.lower()] = dict()
        if 'users' not in self.dict['list'][channel.lower()]:
            self.dict['list'][channel.lower()]['users'] = []
        if nick_id in self.dict['list'][channel.lower()]['users']:
            self.dict['list'][channel.lower()]['users'].remove(nick_id)

    def remove_all_from_channel(self, channel):
        channel = str(channel)
        if channel.lower() not in list(self.dict['list'].keys()):
            self.dict['list'][channel.lower()] = dict()
        if 'users' not in self.dict['list'][channel.lower()]:
            self.dict['list'][channel.lower()]['users'] = []
        self.dict['list'][channel.lower()]['users'] = []
        if channel.lower() in self.channels:
            self.channels.remove(channel.lower())

    def channel_scan(self, bot):
        for channel in list(bot.channels.keys()):
            for user in list(bot.channels[channel].privileges.keys()):
                self.add_to_channel(channel, user)

    def join(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            for user in list(bot.channels[trigger.sender].privileges.keys()):
                self.add_to_channel(trigger.sender, user)
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is in the channel list
        self.add_to_channel(trigger.sender, trigger.nick, nick_id)

    def quit(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            self.remove_all_from_channel(trigger.sender)
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is not in the channel list
        self.remove_from_channel(trigger.sender, trigger.nick, nick_id)

    def part(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            self.remove_all_from_channel(trigger.sender)
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is not in the channel list
        self.remove_from_channel(trigger.sender, trigger.nick, nick_id)

    def kick(self, bot, trigger):
        targetnick = Identifier(str(trigger.args[1]))
        # bot block
        if targetnick == bot.nick:
            self.remove_all_from_channel(trigger.sender)
            return
        # Identify
        nick_id = self.whois_ident(targetnick)
        # Verify nick is not in the channel list
        self.remove_from_channel(trigger.sender, targetnick, nick_id)

    def nick(self, bot, trigger):
        newnick = Identifier(trigger)
        # bot block
        if trigger.nick == bot.nick or newnick == bot.nick:
            return
        # alias the nick
        if not botdb.check_nick_id(newnick):
            botdb.alias_nick(trigger.nick, newnick)
        # Identify
        nick_id = self.whois_ident(newnick)
        # Verify nick is in the channel list
        self.add_to_channel(trigger.sender, trigger.nick, nick_id)

    def mode(self, bot, trigger):
        return

    def check_channel_bot(self, channel, allchan=False):
        if str(channel).lower() in self.channels:
            return True
        elif allchan and str(channel).lower() in list(self.dict['list'].keys()):
            return True
        else:
            return False


channels = BotChannels()
