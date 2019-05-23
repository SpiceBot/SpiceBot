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

    def args(self, command_type='module_command'):
        def actual_decorator(function):
            @functools.wraps(function)
            def argsbuilder(bot, trigger, *args, **kwargs):
                trigger.argcommand, trigger.arglist, trigger.command_type = self.sopel_triggerargs(bot, trigger, command_type)
                return function(bot, trigger, *args, **kwargs)
            return argsbuilder
        return actual_decorator

    def sopel_triggerargs(self, bot, trigger, command_type='module_command'):
        triggerargs = spicemanip.main(trigger.args[1], 'create')
        if command_type in ['nickname', 'nickname_command', 'nickname_commands']:
            command = spicemanip.main(triggerargs, 2).lower()
            triggerargs = spicemanip.main(triggerargs, '3+', 'list')
        else:
            command = spicemanip.main(triggerargs, 1).lower()[1:]
            triggerargs = spicemanip.main(triggerargs, '2+', 'list')
        return triggerargs, command, command_type


prerun = BotPrerun()
