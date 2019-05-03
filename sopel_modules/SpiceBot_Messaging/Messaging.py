# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.osd
import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, command_permissions_check, inlist


def configure(config):
    pass


def setup(bot):
    pass


@sopel.module.nickname_commands('action', 'notice', 'privmsg')
def bot_command_hub(bot, trigger):

    if not command_permissions_check(bot, trigger, ['admins', 'owner']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    if not len(triggerargs):
        bot.say("You must specify a channel.")
        return

    channel = spicemanip.main(triggerargs, 1)
    if not inlist(bot, channel.lower(), bot.memory['SpiceBot_Channels']['channels'].keys()) and channel != 'all':
        bot.osd("Channel name {} not valid.".format(channel))
        return

    triggerargs = spicemanip.main(triggerargs, '2+')

    if channel == 'all':
        channelsendlist = bot.channels.keys()
    else:
        channelsendlist = [channel]

    botmessage = spicemanip.main(triggerargs, 0)
    if not botmessage:
        bot.say("You must specify a message to send.")
        return

    bot.osd(botmessage, channelsendlist, triggercommand.upper())
