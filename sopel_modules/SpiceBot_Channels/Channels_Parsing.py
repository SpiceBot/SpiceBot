# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_SBTools import topic_compile


@sopel.module.event('321')
@sopel.module.rule('.*')
def watch_chanlist_start(bot, trigger):
    bot.memory['SpiceBot_Channels']['ProcessLock'] = True


@sopel.module.event('322')
@sopel.module.rule('.*')
def watch_chanlist_populate(bot, trigger):
    channel, _, topic = trigger.args[1:]
    if channel.lower() not in bot.memory['SpiceBot_Channels']['channels']:
        bot.memory['SpiceBot_Channels']['channels'][channel.lower()] = dict()
        bot.memory['SpiceBot_Channels']['channels'][channel.lower()]['name'] = channel
        bot.memory['SpiceBot_Channels']['channels'][channel.lower()]['topic'] = topic_compile(topic)
    bot.memory['SpiceBot_Channels']['ProcessLock'] = True


@sopel.module.event('323')
@sopel.module.rule('.*')
def watch_chanlist_complete(bot, trigger):
    bot.memory['SpiceBot_Channels']['ProcessLock'] = False
    if not bot.memory['SpiceBot_Channels']['InitialProcess']:
        bot.memory['SpiceBot_Channels']['InitialProcess'] = True
