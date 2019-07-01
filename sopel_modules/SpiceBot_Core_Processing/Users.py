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


@sopel.module.rule('.*')
def bot_users_chat(bot, trigger):
    SpiceBot.users.chat(bot, trigger)
