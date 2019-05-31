# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute

import re
import threading
import time

import spicemanip

from .Config import config as botconfig
from .Events import events
from .Logs import logs


class SpiceBot_Channels_MainSection(StaticSection):
    announcenew = ValidatedAttribute('announcenew', default=False)
    joinall = ValidatedAttribute('joinall', default=False)
    operadmin = ValidatedAttribute('operadmin', default=False)
    chanignore = ListAttribute('chanignore')


class BotChannels():
    """This Logs all channels known to the server"""
    def __init__(self):

        # SpiceBot
        logs.log('SpiceBot_Channels', "Setting Up BotChannels class")
        botconfig.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
        events.startup_add([events.BOT_CHANNELS])

        self.lock = threading.Lock()
        self.channel_lock = False
        self.dict = {
                    "list": {},
                    "InitialProcess": False
                    }

    def channel_list_request(self, bot):
        bot.write(['LIST'])

    def channel_list_recieve_start(self):
        self.channel_lock = True

    def channel_list_recieve_input(self, trigger):
        self.lock.acquire()
        channel, _, topic = trigger.args[1:]
        if channel.lower() not in self.dict['list'].keys():
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
        for channel in bot.channels.keys():
            if len(bot.channels[channel].privileges.keys()) == 1 and channel not in ignorepartlist and channel.startswith("#"):
                bot.part(channel, "Leaving Empty Channel")
                if channel.lower() in self.dict['list']:
                    self.lock.acquire()
                    del self.dict['list'][channel.lower()]
                    self.lock.release()

    def join_all_channels(self, bot):
        if bot.config.SpiceBot_Channels.joinall:
            for channel in self.dict['list'].keys():
                if channel.startswith("#"):
                    if channel not in bot.channels.keys() and channel not in bot.config.SpiceBot_Channels.chanignore:
                        bot.write(('JOIN', bot.nick, self.dict['list'][channel]['name']))
                        if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                            bot.write(('SAJOIN', bot.nick, self.dict['list'][channel]['name']))

    def chanadmin_all_channels(self, bot):
        # Chan ADMIN +a
        for channel in bot.channels.keys():
            if channel.startswith("#"):
                if channel not in bot.config.SpiceBot_Channels.chanignore:
                    if bot.config.SpiceBot_Channels.operadmin:
                        if not bot.channels[channel].privileges[bot.nick] < sopel.module.ADMIN:
                            bot.write(('SAMODE', channel, "+a", bot.nick))
                else:
                    bot.part(channel)


channels = BotChannels()


@sopel.module.event(events.RPL_WELCOME)
@sopel.module.rule('.*')
def unkickable_bot(bot, trigger):
    if bot.config.SpiceBot_Channels.operadmin:
        bot.write(('SAMODE', bot.nick, '+q'))


@sopel.module.event(events.RPL_WELCOME)
@sopel.module.rule('.*')
def request_channels_list_initial(bot, trigger):

    channels.bot_part_empty(bot)

    logs.log('SpiceBot_Channels', "Sending Request for all server channels")
    channels.channel_list_request(bot)

    starttime = time.time()

    # wait 60 seconds for initial population of information
    while not channels.dict['InitialProcess']:
        if time.time() - starttime >= 60:
            logs.log('SpiceBot_Channels', "Initial Channel list populating Timed Out")
            channels.dict['InitialProcess'] = True
        else:
            pass

    foundchannelcount = len(channels.dict['list'].keys())
    logs.log('SpiceBot_Channels', "Channel listing finished! " + str(foundchannelcount) + " channel(s) found.")

    channels.join_all_channels(bot)
    channels.chanadmin_all_channels(bot)

    if "*" in channels.dict['list'].keys():
        del channels.dict['list']["*"]

    channels.bot_part_empty(bot)
    events.trigger(bot, events.BOT_CHANNELS, "SpiceBot_Channels")


@sopel.module.event('321')
@sopel.module.rule('.*')
def watch_chanlist_start(bot, trigger):
    channels.channel_list_recieve_start()


@sopel.module.event('322')
@sopel.module.rule('.*')
def watch_chanlist_populate(bot, trigger):
    channels.channel_list_recieve_input(trigger)


@sopel.module.event('323')
@sopel.module.rule('.*')
def watch_chanlist_complete(bot, trigger):
    channels.channel_list_recieve_finish()


@sopel.module.event(events.BOT_CHANNELS)
@sopel.module.rule('.*')
def trigger_channel_list_recurring(bot, trigger):
    while True:
        time.sleep(1800)
        channels.bot_part_empty(bot)

        oldlist = list(channels.dict['list'].keys())
        channels.channel_list_request(bot)

        while channels.channel_lock:
            pass

        newlist = [item.lower() for item in oldlist if item.lower() not in list(channels.dict['list'].keys())]
        if "*" in newlist:
            newlist.remove("*")
        if len(newlist) and bot.config.SpiceBot_Channels.announcenew:
            bot.osd(["The Following channel(s) are new:", spicemanip.main(newlist, 'andlist')], bot.channels.keys())

        channels.join_all_channels(bot)

        channels.chanadmin_all_channels(bot)

        if "*" in channels.dict['list'].keys():
            del channels.dict['list']["*"]
        channels.bot_part_empty(bot)
