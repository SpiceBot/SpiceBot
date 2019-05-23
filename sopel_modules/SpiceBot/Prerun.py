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

    def prerun(self, trigger_command_type='module_command'):
        def actual_decorator(function):
            @functools.wraps(function)
            def internal_prerun(bot, trigger, *args, **kwargs):
                prerun_split = self.sopel_trigger_args(bot, trigger, trigger_command_type)
                for argsdict in prerun_split:
                    trigger.sb = argsdict
                    function(bot, trigger, *args, **kwargs)
                return
            return internal_prerun
        return actual_decorator

    def sopel_trigger_args(self, bot, trigger, trigger_command_type='module_command'):

        trigger_args = spicemanip.main(trigger.args[1], 'create')
        if trigger_command_type in ['nickname', 'nickname_command', 'nickname_commands']:
            trigger_command = spicemanip.main(trigger_args, 2).lower()
            trigger_args = spicemanip.main(trigger_args, '3+', 'list')
        else:
            trigger_command = spicemanip.main(trigger_args, 1).lower()[1:]
            trigger_args = spicemanip.main(trigger_args, '2+', 'list')

        # Handle && splittings
        trigger_args_list_split = spicemanip.main(trigger_args, "split_&&")
        if not len(trigger_args_list_split):
            trigger_args_list_split.append([])

        prerun_split = []
        for trigger_args_list in trigger_args_list_split:
            trigger_args_part = spicemanip.main(trigger_args_list, 'create')
            argsdict = {"com": trigger_command, "args": trigger_args_part, "type": trigger_command_type}
            prerun_split.append(argsdict)

        return prerun_split


prerun = BotPrerun()
