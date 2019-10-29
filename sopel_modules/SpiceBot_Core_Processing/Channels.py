# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel

import time
from threading import Thread

from sopel_modules.spicemanip import spicemanip

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
    while not SpiceBot.channels.InitialProcess:
        if time.time() - starttime >= 60:
            SpiceBot.logs.log('SpiceBot_Channels', "Initial Channel list populating Timed Out")
            SpiceBot.channels.InitialProcess = True
        else:
            pass

    foundchannelcount = SpiceBot.channels.total_channels()
    SpiceBot.logs.log('SpiceBot_Channels', "Channel listing finished! " + str(foundchannelcount) + " channel(s) found.")

    SpiceBot.channels.join_all_channels(bot)

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
    Thread(target=channels_thread, args=(bot,)).start()


def channels_thread(bot):
    while True:
        time.sleep(1800)
        SpiceBot.channels.bot_part_empty(bot)

        oldlist = SpiceBot.channels.chanlist()
        SpiceBot.channels.channel_list_request(bot)

        while SpiceBot.channels.channel_lock:
            pass

        currentlist = SpiceBot.channels.chanlist()
        newlist = []
        for channel in currentlist:
            if channel not in oldlist:
                newlist.append(channel)
        if "*" in newlist:
            newlist.remove("*")
        if len(newlist) and SpiceBot.config.SpiceBot_Channels.announcenew:
            bot.osd(["The Following channel(s) are new:", spicemanip(newlist, 'andlist')], list(bot.channels.keys()))

        SpiceBot.channels.join_all_channels(bot)

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
    SpiceBot.channels.channel_scan(bot)


@sopel.module.event(SpiceBot.events.RPL_NAMREPLY)
@sopel.module.rule('(.*)')
def handle_names_channels(bot, trigger):
    SpiceBot.channels.rpl_names(bot, trigger)


@sopel.module.event(SpiceBot.events.RPL_WHOREPLY)
@sopel.module.rule('.*')
@sopel.module.priority('high')
@sopel.module.unblockable
def recv_who_channels(bot, trigger):
    SpiceBot.channels.rpl_who(bot, trigger)
