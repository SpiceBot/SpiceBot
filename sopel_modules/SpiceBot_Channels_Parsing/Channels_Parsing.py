#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents
from sopel_modules.SpiceBot.Channels import botchannels

import spicemanip

import time


class SpiceBot_Channels_MainSection(StaticSection):
    announcenew = ValidatedAttribute('announcenew', default=False)
    joinall = ValidatedAttribute('joinall', default=False)
    operadmin = ValidatedAttribute('operadmin', default=False)
    chanignore = ListAttribute('chanignore')


def configure(config):
    config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
    config.SpiceBot_Channels.configure_setting('announcenew', 'SpiceBot_Channels Announce New Channels')
    config.SpiceBot_Channels.configure_setting('joinall', 'SpiceBot_Channels JOIN New Channels')
    config.SpiceBot_Channels.configure_setting('operadmin', 'SpiceBot_Channels OPER ADMIN MODE')
    config.SpiceBot_Channels.configure_setting('chanignore', 'SpiceBot_Channels Ignore JOIN for channels')


def setup(bot):
    botlogs.log('SpiceBot_Channels', "Starting setup procedure")
    botevents.startup_add([botevents.BOT_CHANNELS])
    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)


@sopel.module.event(botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def unkickable_bot(bot, trigger):
    if bot.config.SpiceBot_Channels.operadmin:
        bot.write(('SAMODE', bot.nick, '+q'))


@sopel.module.event(botevents.RPL_WELCOME)
@sopel.module.rule('.*')
def request_channels_list_initial(bot, trigger):

    botchannels.bot_part_empty(bot)

    botlogs.log('SpiceBot_Channels', "Sending Request for all server channels")
    botchannels.channel_list_request(bot)

    starttime = time.time()

    # wait 60 seconds for initial population of information
    while not botchannels.SpiceBot_Channels['InitialProcess']:
        if time.time() - starttime >= 60:
            botlogs.log('SpiceBot_Channels', "Initial Channel list populating Timed Out")
            botchannels.SpiceBot_Channels['InitialProcess'] = True
        else:
            pass

    foundchannelcount = len(botchannels.SpiceBot_Channels['list'].keys())
    botlogs.log('SpiceBot_Channels', "Channel listing finished! " + str(foundchannelcount) + " channel(s) found.")

    botchannels.join_all_channels(bot)
    botchannels.chanadmin_all_channels(bot)

    if "*" in botchannels.SpiceBot_Channels['list'].keys():
        del botchannels.SpiceBot_Channels['list']["*"]

    botchannels.bot_part_empty(bot)
    botevents.trigger(bot, botevents.BOT_CHANNELS, "SpiceBot_Channels")


@sopel.module.event('321')
@sopel.module.rule('.*')
def watch_chanlist_start(bot, trigger):
    botchannels.channel_list_recieve_start()


@sopel.module.event('322')
@sopel.module.rule('.*')
def watch_chanlist_populate(bot, trigger):
    botchannels.channel_list_recieve_input(trigger)


@sopel.module.event('323')
@sopel.module.rule('.*')
def watch_chanlist_complete(bot, trigger):
    botchannels.channel_list_recieve_finish()


@sopel.module.event(botevents.BOT_CHANNELS)
@sopel.module.rule('.*')
def trigger_channel_list_recurring(bot, trigger):
    while True:
        time.sleep(1800)
        botchannels.bot_part_empty(bot)

        oldlist = list(botchannels.SpiceBot_Channels['list'].keys())
        botchannels.channel_list_request(bot)

        while botchannels.channel_lock:
            pass

        newlist = [item.lower() for item in oldlist if item.lower() not in list(botchannels.SpiceBot_Channels['list'].keys())]
        if "*" in newlist:
            newlist.remove("*")
        if len(newlist) and bot.config.SpiceBot_Channels.announcenew:
            bot.osd(["The Following channel(s) are new:", spicemanip.main(newlist, 'andlist')], bot.channels.keys())

        botchannels.join_all_channels(bot)

        botchannels.chanadmin_all_channels(bot)

        if "*" in botchannels.SpiceBot_Channels['list'].keys():
            del botchannels.SpiceBot_Channels['list']["*"]
        botchannels.bot_part_empty(bot)
