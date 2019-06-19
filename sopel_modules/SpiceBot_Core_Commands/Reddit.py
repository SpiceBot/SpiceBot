# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.rule(r"""(?:)u/
          (
            (?:\\/ | [^/])+
          )
          """)
@sopel.module.rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_user(bot, trigger):
    bot.say(str(trigger.group(0)))
    bot.say(str(trigger.group(1)))
    bot.say(str(trigger.group(2)))
    bot.say(str(trigger.group(3)))
    bot.say(str(trigger.group(4)))
    bot.say(str(trigger.group(5)))
    message = SpiceBot.reddit.prerun(trigger)
    bot.osd(str(message))
