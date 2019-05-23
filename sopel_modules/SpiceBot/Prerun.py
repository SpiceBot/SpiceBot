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

    def args(self, trigger_command_type='module_command'):
        def actual_decorator(function):
            @functools.wraps(function)
            def argsbuilder(bot, trigger, *args, **kwargs):
                trigger.sb = self.sopel_trigger_args(bot, trigger, trigger_command_type)
                return function(bot, trigger, *args, **kwargs)
            return argsbuilder
        return actual_decorator

    def sopel_trigger_args(self, bot, trigger, trigger_command_type='module_command'):
        trigger_args = spicemanip.main(trigger.args[1], 'create')
        if trigger_command_type in ['nickname', 'nickname_command', 'nickname_commands']:
            trigger_command = spicemanip.main(trigger_args, 2).lower()
            trigger_args = spicemanip.main(trigger_args, '3+', 'list')
        else:
            trigger_command = spicemanip.main(trigger_args, 1).lower()[1:]
            trigger_args = spicemanip.main(trigger_args, '2+', 'list')
        argsdict = {"com": trigger_command, "args": trigger_args, "type": trigger_command_type}
        return argsdict


prerun = BotPrerun()
