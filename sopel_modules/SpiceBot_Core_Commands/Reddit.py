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
    trigger = reddit_prerun(trigger)
    bot.osd(str(trigger.sb))


@sopel.module.rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
def bot_command_reddit_subreddit(bot, trigger):
    trigger = reddit_prerun(trigger)
    bot.osd(str(trigger.sb))


def reddit_prerun(trigger):
    trigger_args = spicemanip.main(trigger.args[1], 'create')
    trigger.sb = {
                    "slashcomm": spicemanip.main(trigger_args, 1).lower()[:1],
                    "command": spicemanip.main(trigger_args, 1).lower()[2:],
                    "args": spicemanip.main(trigger_args, "2+", 'list').lower()
                    }
    return trigger
