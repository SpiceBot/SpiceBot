# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


# @rule(r"^(r|u)\/([^\s/]+)") TODO


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOADED])
@sopel.module.rule(r"""(?:)u/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_user(bot, trigger):
    message = SpiceBot.reddit.prerun(trigger)
    bot.osd(message)


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOADED])
@sopel.module.rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_subreddit(bot, trigger):
    message = SpiceBot.reddit.prerun(trigger)
    bot.osd(message)
