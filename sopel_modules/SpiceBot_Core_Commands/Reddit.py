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
    trigger_command = spicemanip.main(trigger.args[1], 1).lower()[0:]
    bot.osd(str(trigger_command))


@sopel.module.rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_subreddit(bot, trigger):
    bot.osd(str(trigger))
    bot.osd(str(trigger.args))
