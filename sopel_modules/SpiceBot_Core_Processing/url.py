# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Logs system.
"""
import sopel


@sopel.module.url('(.*)')
def watch_url(bot, trigger):

    bot.osd(str(trigger))
    bot.osd(str(trigger.args))
