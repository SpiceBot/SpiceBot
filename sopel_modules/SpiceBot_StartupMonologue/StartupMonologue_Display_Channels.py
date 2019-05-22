# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_CHANNELS)
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):

    botcount = len(bot.channels.keys())
    servercount = len(SpiceBot.channels.dict['list'].keys())
    bot.memory['SpiceBot_StartupMonologue'].append("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")
    SpiceBot.logs.log('SpiceBot_StartupMonologue', "I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_STARTUPMONOLOGUE_CHANNELS, "SpiceBot_StartupMonologue")
