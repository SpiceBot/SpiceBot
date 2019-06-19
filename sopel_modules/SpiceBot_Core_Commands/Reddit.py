# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import spicemanip

# import sopel_modules.SpiceBot as SpiceBot


@sopel.module.rule(r"""(?:)u/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_user(bot, trigger):
    trigger_command = spicemanip.main(trigger.args[1], 1).lower()[:1]
    trigger_arg = spicemanip.main(trigger.args[1], 1).lower()[1:]
    bot.osd(str(trigger_command))
    bot.osd(str(trigger_arg))


@sopel.module.rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_subreddit(bot, trigger):
    bot.osd(str(trigger))
    bot.osd(str(trigger.args))
