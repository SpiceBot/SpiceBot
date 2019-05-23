# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Prerun system.
"""

import functools
import spicemanip


class BotPrerun():
    def __init__(self):
        self.dict = {}

    def args(level, message=None, reply=False):
        def actual_decorator(function):
            @functools.wraps(function)
            def argsbuilder(bot, trigger, *args, **kwargs):
                triggerargs = spicemanip.main(trigger.args[1], 'create')
                if triggerargs[0].lower() == bot.nick.lower():
                    trigger.command = spicemanip.main(triggerargs, 2).lower()
                    trigger.arglist = spicemanip.main(triggerargs, '3+', 'list')
                else:
                    trigger.command = spicemanip.main(triggerargs, 1).lower()[1:]
                    trigger.arglist = spicemanip.main(triggerargs, '2+', 'list')
                return function(bot, trigger, *args, **kwargs)
            return argsbuilder
        return actual_decorator


prerun = BotPrerun()
