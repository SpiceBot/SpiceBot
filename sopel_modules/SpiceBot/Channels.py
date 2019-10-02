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

# replace process lock with uuid list system


class BotChannels():
    """This Logs all channels known to the server"""
    def __init__(self):

        # bot config setup
        self.setup_channels()

        # Locking
        self.lock = threading.Lock()
        self.channel_lock = False

        # list of channels
        self.chandict = {}

        # list of uuids to process
        self.server_recieved = []

        # initial process
        self.InitialProcess = False

        self.who_reqs = {}

    def total_channels(self):
        totalcount = len(list(self.chandict.keys()))
        return totalcount

    def total_bot_channels(self):
        totalcount = 0
        for channel in list(self.chandict.keys()):
            if self.chandict[channel]["joined"]:
                totalcount += 1
        return totalcount

    def chanlist(self):
        return list(self.chandict.keys())

    def chanlist_bot(self):
        chanlist_return = []
        for channel in list(self.chandict.keys()):
            if self.chandict[channel]["joined"]:
                chanlist_return.append(channel)
        return chanlist_return

    def ischannel(self, channel):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        if channel in list(self.chandict.keys()):
            return True
        else:
            return False

    def get_channel_users(self, channel):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        # channel not on server
        if channel not in list(self.chandict.keys()):
            raise Exception('Channel ' + str(channel) + " does not seem to be on this server")

        # bot is not in channel
        if not self.chandict[channel]["joined"]:
            raise Exception('Channel ' + str(channel) + " does not seem to be a channel the bot is in")

        return self.chandict[channel]["users"]

    def setup_channels(self):
        botconfig.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)

    def channel_list_request(self, bot):
        bot.write(['LIST'])

    def channel_list_recieve_start(self):
        self.channel_lock = True

    def channel_list_recieve_input(self, trigger):

        # parse info
        channel, _, topic = trigger.args[1:]

        # check channel existance
        if channel not in list(self.chandict.keys()):
            self.channeldict_append(channel)

        self.lock.acquire()

        # get proper name of channel
        self.chandict[channel.lower()]['name'] = channel
        self.chandict[channel.lower()]['topic'] = self.topic_compile(topic)
        self.channel_lock = True
        self.lock.release()

    def channel_list_recieve_finish(self):
        self.lock.acquire()
        if not self.InitialProcess:
            self.InitialProcess = True
        self.channel_lock = False
        self.lock.release()

    def topic_compile(self, topic):
        actual_topic = re.compile(r'^\[\+[a-zA-Z]+\] (.*)')
        topic = re.sub(actual_topic, r'\1', topic)
        if topic.isspace():
            topic = None
        return topic

    def channeldict_append(self, channel):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        # create basic components of the channel dict
        self.lock.acquire()
        if channel not in list(self.chandict.keys()):
            self.chandict[channel] = {
                                        "name": channel,
                                        "topic": None,
                                        "joined": False,
                                        "reason": "appended",
                                        "users": [],
                                        }
        self.lock.release()

    def add_channel(self, channel, reason=None):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        # check channel existance
        if channel not in list(self.chandict.keys()):
            self.channeldict_append(channel)

        self.lock.acquire()
        if reason != "check":
            self.chandict[channel]["joined"] = True
            self.chandict[channel]["reason"] = reason
        self.lock.release()

    def remove_channel(self, channel, reason=None):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        # check channel existance
        if channel not in list(self.chandict.keys()):
            self.channeldict_append(channel)

        self.lock.acquire()
        if reason != "check":
            self.chandict[channel]["joined"] = False
            self.chandict[channel]["reason"] = reason
        self.lock.release()

    def bot_part_empty(self, bot):
        """Don't stay in empty channels"""
        ignorepartlist = []  # TODO add bot.config channels to ignore
        if bot.config.core.logging_channel:
            ignorepartlist.append(bot.config.core.logging_channel)
        for channel in list(bot.channels.keys()):
            if channel.startswith("#") and channel not in ignorepartlist:
                if len(list(bot.channels[channel].privileges.keys())) == 1:
                    bot.part(channel, "Leaving Empty Channel")
                    if channel.lower() in list(self.chandict.keys()):
                        self.lock.acquire()
                        self.chandict[channel]["joined"] = False
                        self.chandict[channel]["reason"] = "empty_chan_part"
                        self.lock.release()
                    self.remove_channel(channel)

    def join_all_channels(self, bot):
        if botconfig.SpiceBot_Channels.joinall:
            for channel in list(self.chandict.keys()):
                if channel.startswith("#") and channel not in botconfig.SpiceBot_Channels.chanignore:
                    if channel.lower() not in [chan.lower() for chan in list(bot.channels.keys())]:
                        self.bot_join(bot, channel)
                        if channel.lower() not in [chan.lower() for chan in list(bot.channels.keys())]:
                            self.bot_sajoin(bot, channel)

    def bot_join(self, bot, channel):
        bot.write(('JOIN', bot.nick, channel))

    def bot_sajoin(self, bot, channel):
        if botconfig.SpiceBot_Channels.operadmin:
            bot.write(('SAJOIN', bot.nick, channel))

    def chanadmin_channel(self, bot, channel):
        # Chan ADMIN +a
        if botconfig.SpiceBot_Channels.operadmin:
            if not bot.channels[channel].privileges[bot.nick] < sopel.module.ADMIN:
                bot.write(('SAMODE', channel, "+a", bot.nick))

    def whois_ident(self, nick):
        nick = Identifier(nick)
        nick_id = botusers.get_nick_id(nick, True)
        return nick_id

    def add_to_channel(self, channel, nick, nick_id=None):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        # Verify Channel is in list
        if channel not in list(self.chandict.keys()):
            self.add_channel(channel, "error_handling")

        self.lock.acquire()
        if not nick_id:
            nick_id = self.whois_ident(nick)
        if int(nick_id) not in self.chandict[channel]["users"]:
            self.chandict[channel]["users"].append(int(nick_id))
        self.lock.release()

    def remove_from_channel(self, channel, nick, nick_id=None):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        # Verify Channel is in list
        if channel not in list(self.chandict.keys()):
            self.add_channel(channel, "error_handling")

        self.lock.acquire()
        if not nick_id:
            nick_id = self.whois_ident(nick)
        if int(nick_id) in self.chandict[channel.lower()]['users']:
            self.chandict[channel.lower()]['users'].remove(int(nick_id))
        self.lock.release()

    def remove_all_from_channel(self, channel):

        # channel names case-sensitivity should never be an issue
        channel = str(channel).lower()

        # Verify Channel is in list
        if channel not in list(self.chandict.keys()):
            self.add_channel(channel, "error_handling")

        self.lock.acquire()
        self.chandict[channel.lower()]['users'] = []
        self.lock.release()

    def channel_scan(self, bot):
        for channel in list(bot.channels.keys()):
            for user in list(bot.channels[channel].privileges.keys()):
                self.add_to_channel(channel, user)

    def join(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            self.chanadmin_channel(bot, trigger.sender)
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
            self.lock.acquire()
            self.chandict[trigger.sender]["joined"] = False
            self.chandict[trigger.sender]["reason"] = "quit"
            self.lock.release()
            return
        # Identify
        nick_id = self.whois_ident(trigger.nick)
        # Verify nick is not in the channel list
        self.remove_from_channel(trigger.sender, trigger.nick, nick_id)

    def part(self, bot, trigger):
        # bot block
        if trigger.nick == bot.nick:
            self.remove_all_from_channel(trigger.sender)
            self.lock.acquire()
            self.chandict[trigger.sender]["joined"] = False
            self.chandict[trigger.sender]["reason"] = "bot_part"
            self.lock.release()
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
            self.lock.acquire()
            self.chandict[trigger.sender]["joined"] = False
            self.chandict[trigger.sender]["reason"] = "kicked"
            self.lock.release()
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

    def rpl_names(self, bot, trigger):
        """Handle NAMES response, happens when joining to channels."""
        names = trigger.split()

        # TODO specific to one channel type. See issue 281.
        channels = re.search(r'(#\S*)', trigger.raw)
        if not channels:
            return
        channel = Identifier(channels.group(1))
        self.add_channel(channel)

        mapping = {'+': sopel.module.VOICE,
                   '%': sopel.module.HALFOP,
                   '@': sopel.module.OP,
                   '&': sopel.module.ADMIN,
                   '~': sopel.module.OWNER}

        for name in names:
            nick = Identifier(name.lstrip(''.join(mapping.keys())))
            self.add_to_channel(channel, nick)

    def rpl_who(self, bot, trigger):
        if len(trigger.args) < 2 or trigger.args[1] not in self.who_reqs:
            # Ignored, some module probably called WHO
            return
        if len(trigger.args) != 8:
            return
        _, _, channel, user, host, nick, status, account = trigger.args
        nick = Identifier(nick)
        channel = Identifier(channel)
        self.add_to_channel(channel, nick)

    def check_channel_bot(self, channel, allchan=False):
        if str(channel).lower() in self.chanlist_bot():
            return True
        elif allchan and str(channel).lower() in self.chanlist():
            return True
        else:
            return False


channels = BotChannels()
