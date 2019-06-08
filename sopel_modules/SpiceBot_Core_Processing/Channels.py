# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel

import time

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def unkickable_bot(bot, trigger):
    if SpiceBot.config.SpiceBot_Channels.operadmin:
        bot.write(('SAMODE', bot.nick, '+q'))


@sopel.module.event(SpiceBot.events.RPL_WELCOME)
@sopel.module.rule('.*')
def request_channels_list_initial(bot, trigger):

    SpiceBot.channels.bot_part_empty(bot)

    SpiceBot.logs.log('SpiceBot_Channels', "Sending Request for all server channels")
    SpiceBot.channels.channel_list_request(bot)

    starttime = time.time()

    # wait 60 seconds for initial population of information
    while not SpiceBot.channels.dict['InitialProcess']:
        if time.time() - starttime >= 60:
            SpiceBot.logs.log('SpiceBot_Channels', "Initial Channel list populating Timed Out")
            SpiceBot.channels.dict['InitialProcess'] = True
        else:
            pass

    foundchannelcount = len(list(SpiceBot.channels.dict['list'].keys()))
    SpiceBot.logs.log('SpiceBot_Channels', "Channel listing finished! " + str(foundchannelcount) + " channel(s) found.")

    SpiceBot.channels.join_all_channels(bot)
    SpiceBot.channels.chanadmin_all_channels(bot)

    if "*" in SpiceBot.channels.dict['list'].keys():
        del SpiceBot.channels.dict['list']["*"]

    SpiceBot.channels.bot_part_empty(bot)
    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_CHANNELS, "SpiceBot_Channels")


@sopel.module.event('321')
@sopel.module.rule('.*')
def watch_chanlist_start(bot, trigger):
    SpiceBot.channels.channel_list_recieve_start()


@sopel.module.event('322')
@sopel.module.rule('.*')
def watch_chanlist_populate(bot, trigger):
    SpiceBot.channels.channel_list_recieve_input(trigger)


@sopel.module.event('323')
@sopel.module.rule('.*')
def watch_chanlist_complete(bot, trigger):
    SpiceBot.channels.channel_list_recieve_finish()


@sopel.module.event(SpiceBot.events.BOT_CHANNELS)
@sopel.module.rule('.*')
def trigger_channel_list_recurring(bot, trigger):
    while True:
        time.sleep(1800)
        SpiceBot.channels.bot_part_empty(bot)

        oldlist = list(SpiceBot.channels.dict['list'].keys())
        SpiceBot.channels.channel_list_request(bot)

        while SpiceBot.channels.channel_lock:
            pass

        newlist = [item.lower() for item in oldlist if item.lower() not in list(SpiceBot.channels.dict['list'].keys())]
        if "*" in newlist:
            newlist.remove("*")
        if len(newlist) and SpiceBot.config.SpiceBot_Channels.announcenew:
            bot.osd(["The Following channel(s) are new:", spicemanip.main(newlist, 'andlist')], list(bot.channels.keys()))

        SpiceBot.channels.join_all_channels(bot)

        SpiceBot.channels.chanadmin_all_channels(bot)

        if "*" in list(SpiceBot.channels.dict['list'].keys()):
            del SpiceBot.channels.dict['list']["*"]
        SpiceBot.channels.bot_part_empty(bot)


@sopel.module.event('JOIN')
@sopel.module.rule('.*')
def channels_users_join(bot, trigger):
    SpiceBot.channels.join(bot, trigger)


@sopel.module.event('QUIT')
@sopel.module.rule('.*')
def channels_users_quit(bot, trigger):
    SpiceBot.channels.quit(bot, trigger)


@sopel.module.event('PART')
@sopel.module.rule('.*')
def channels_users_part(bot, trigger):
    SpiceBot.channels.part(bot, trigger)


@sopel.module.event('KICK')
@sopel.module.rule('.*')
def channels_users_kick(bot, trigger):
    SpiceBot.channels.kick(bot, trigger)


@sopel.module.event('NICK')
@sopel.module.rule('.*')
def channels_users_nick(bot, trigger):
    SpiceBot.channels.nick(bot, trigger)


@sopel.module.event('MODE')
@sopel.module.rule('.*')
def channels_users_mode(bot, trigger):
    SpiceBot.channels.mode(bot, trigger)
    # TODO


@sopel.module.event(SpiceBot.events.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_channelscan(bot, trigger):
    while True:
        SpiceBot.channels.channel_scan(bot)
