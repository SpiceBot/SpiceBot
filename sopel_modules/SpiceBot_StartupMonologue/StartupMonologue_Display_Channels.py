# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot.Events import botevents
from sopel_modules.SpiceBot.Channels import botchannels


@sopel.module.event(botevents.BOT_CHANNELS)
@sopel.module.rule('.*')
def bot_startup_monologue_channels(bot, trigger):

    botcount = len(bot.channels.keys())
    servercount = len(botchannels.SpiceBot_Channels['list'].keys())
    bot.memory['SpiceBot_StartupMonologue'].append("I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")
    botlogs.log('SpiceBot_StartupMonologue', "I am in " + str(botcount) + " of " + str(servercount) + " channel(s) available on this server.")

    botevents.trigger(bot, botevents.BOT_STARTUPMONOLOGUE_CHANNELS, "SpiceBot_StartupMonologue")
