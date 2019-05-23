# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Prerun system.
"""

import functools
import copy
import spicemanip


class BotPrerun():
    def __init__(self):
        self.dict = {}

    def prerun(self, trigger_command_type='module_command'):
        def actual_decorator(function):
            @functools.wraps(function)
            def internal_prerun(bot, trigger, *args, **kwargs):

                argsdict_default = {}
                argsdict_default["type"] = trigger_command_type

                # Primary command used for trigger, and a list of all words
                trigger_args, trigger_command = self.trigger_args(trigger.args[1], trigger_command_type)
                argsdict_default["com"] = trigger_command

                # split into && groupings
                and_split = self.and_split(trigger_args)

                # Create dict listings for trigger.sb
                argsdict_list = self.argsdict_create(argsdict_default, and_split)

                # Run the function for all splits
                for argsdict in argsdict_list:
                    trigger.sb = argsdict
                    function(bot, trigger, *args, **kwargs)

                return
            return internal_prerun
        return actual_decorator

    def trigger_args(self, triggerargs_one, trigger_command_type='module_command'):
        trigger_args = spicemanip.main(triggerargs_one, 'create')
        if trigger_command_type in ['nickname', 'nickname_command', 'nickname_commands']:
            trigger_command = spicemanip.main(trigger_args, 2).lower()
            trigger_args = spicemanip.main(trigger_args, '3+', 'list')
        else:
            trigger_command = spicemanip.main(trigger_args, 1).lower()[1:]
            trigger_args = spicemanip.main(trigger_args, '2+', 'list')
        return trigger_args, trigger_command

    def and_split(self, trigger_args):
        trigger_args_list_split = spicemanip.main(trigger_args, "split_&&")
        if not len(trigger_args_list_split):
            trigger_args_list_split.append([])
        return trigger_args_list_split

    def argsdict_list(self, argsdict_default, prerun_and_split):
        prerun_split = []
        for trigger_args_list in prerun_and_split:
            argsdict = copy.deepcopy(argsdict_default)
            trigger_args_part = spicemanip.main(trigger_args_list, 'create')
            argsdict["args"] = trigger_args_part
            prerun_split.append(argsdict)
        return prerun_split


prerun = BotPrerun()
