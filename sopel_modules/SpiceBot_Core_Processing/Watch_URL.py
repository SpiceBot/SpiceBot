# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel


# @sopel.module.url('(.*)')
# @sopel.module.url(r'xkcd.com/(\d+)')
@sopel.module.rule(r'(?u).*(https?://\S+).*')
def watch_url(bot, trigger):

    bot.osd(str(trigger))
    bot.osd(str(trigger.args))
