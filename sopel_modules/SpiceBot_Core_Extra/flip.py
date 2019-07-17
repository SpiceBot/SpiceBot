# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

# import sopel_modules.SpiceBot as SpiceBot

# from sopel_modules.spicemanip import spicemanip

from upsidedown import transform
# TODO add upsidedown to spicemanip
# TODO add prerun functionality as well as command handling


@sopel.module.rule('^flips (.+)')
@sopel.module.intent('ACTION')
def flips(bot, trigger):
    target = trigger.group(1).strip()
    if target == 'a table':
        bot.say("(╯°□°）╯︵ ┻━┻")
    else:
        bot.say("(╯°□°）╯︵ %s" % transform(target))


@sopel.module.rule('^rolls (.+)')
@sopel.module.intent('ACTION')
def roll(bot, trigger):
    target = trigger.group(1).strip()
    if target.endswith(' down a hill'):
        target = target[:-12]
        tegrat = transform(target)
        bot.say("(╮°-°)╯︵ %s %s %s %s %s (@_@;)" % (tegrat, target, tegrat, target, tegrat))
    else:
        bot.say("(╮°-°)╯︵ %s" % transform(target))
