# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event('JOIN')
@sopel.module.rule('.*')
def users_join(bot, trigger):
    SpiceBot.users.join(bot, trigger)


@sopel.module.event('QUIT')
@sopel.module.rule('.*')
def users_quit(bot, trigger):
    SpiceBot.users.quit(bot, trigger)


@sopel.module.event('PART')
@sopel.module.rule('.*')
def users_part(bot, trigger):
    SpiceBot.users.part(bot, trigger)


@sopel.module.event('KICK')
@sopel.module.rule('.*')
def users_kick(bot, trigger):
    SpiceBot.users.kick(bot, trigger)


@sopel.module.event('NICK')
@sopel.module.rule('.*')
def users_nick(bot, trigger):
    SpiceBot.users.nick(bot, trigger)


@sopel.module.event('MODE')
@sopel.module.rule('.*')
def users_mode(bot, trigger):
    SpiceBot.users.mode(bot, trigger)
    # TODO


@sopel.module.event(SpiceBot.events.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_channelscan_users(bot, trigger):
    SpiceBot.users.channel_scan(bot)


"""
@sopel.module.rule('.*')
def bot_users_chat(bot, trigger):
    SpiceBot.users.chat(bot, trigger)


@sopel.module.event(SpiceBot.events.RPL_NAMREPLY)
@sopel.module.rule('(.*)')
def handle_names(bot, trigger):
    SpiceBot.users.rpl_names(bot, trigger)


@sopel.module.event(SpiceBot.events.RPL_WHOREPLY)
@sopel.module.rule('.*')
@sopel.module.priority('high')
@sopel.module.unblockable
def recv_who(bot, trigger):
    SpiceBot.users.rpl_who(bot, trigger)


@sopel.module.event('ACCOUNT')
@sopel.module.rule('.*')
def account_notify(bot, trigger):
    SpiceBot.users.account(bot, trigger)


@sopel.module.event('AWAY')
@sopel.module.rule('.*')
def track_notify(bot, trigger):
    SpiceBot.users.track_notify(bot, trigger)
"""
