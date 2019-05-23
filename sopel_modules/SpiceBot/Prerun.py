# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Prerun system.
"""

from sopel.tools import Identifier

import functools
import copy
import datetime
import spicemanip

from .Tools import command_permissions_check
from .Commands import commands
from .Database import db as spicedb


class BotPrerun():
    def __init__(self):
        self.dict = {}

    def prerun(self, trigger_command_type='module'):
        def actual_decorator(function):
            @functools.wraps(function)
            def internal_prerun(bot, trigger, *args, **kwargs):

                # Bots can't run commands
                if Identifier(trigger.nick) == bot.nick:
                    return

                # Primary command used for trigger, and a list of all words
                trigger_args, trigger_command = self.trigger_args(trigger.args[1], trigger_command_type)

                command_lookup = commands.find_command_type(trigger_command)

                # Argsdict Defaults
                argsdict_default = {}
                argsdict_default["type"] = trigger_command_type
                argsdict_default["com"] = trigger_command

                if command_lookup and "aliasfor" in commands.dict["commands"][command_lookup].keys():
                    realcom = commands.dict["commands"][command_lookup]["aliasfor"]
                else:
                    realcom = trigger_command
                argsdict_default["realcom"] = realcom

                # split into && groupings
                and_split = self.and_split(trigger_args)

                # Create dict listings for trigger.sb
                argsdict_list = self.argsdict_list(argsdict_default, and_split)

                # Run the function for all splits
                for argsdict in argsdict_list:
                    trigger.sb = argsdict

                    if len(argsdict["hyphen_args"]):
                        self.hyphen_arg_handler(bot, trigger, argsdict)

                    # check if anything prohibits the nick from running the command
                    if self.runstatus(bot, trigger, argsdict):
                        function(bot, trigger, *args, **kwargs)
                return
            return internal_prerun
        return actual_decorator

    def trigger_args(self, triggerargs_one, trigger_command_type='module'):
        trigger_args = spicemanip.main(triggerargs_one, 'create')
        if trigger_command_type in ['nickname']:
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

    def argsdict_list(self, argsdict_default, and_split):
        prerun_split = []
        for trigger_args_part in and_split:

            argsdict_part = copy.deepcopy(argsdict_default)

            trigger_args_part_list = spicemanip.main(trigger_args_part, 'create')

            argsdict_part["args"], argsdict_part["hyphen_args"] = self.hyphen_args(trigger_args_part_list)

            prerun_split.append(argsdict_part)
        return prerun_split

    def hyphen_args(self, trigger_args_part):
        valid_hyphen_args = [
                            'enable', 'disable'
                            ]
        hyphen_args = []
        trigger_args_unhyphend = []
        for worditem in trigger_args_part:
            if str(worditem).startswith("--"):
                hyphencom = worditem[2:]
                if hyphencom in valid_hyphen_args:
                    hyphen_args.append(hyphencom)
            else:
                trigger_args_unhyphend.append(worditem)
        return trigger_args_unhyphend, hyphen_args

    def hyphen_arg_handler(self, bot, trigger, argsdict):

        hyphenarg = argsdict["hyphen_args"][0]

        # Commands that cannot run via privmsg
        if hyphenarg in ['enable']:

            if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
                bot.say("I was unable to disable this command due to privilege issues.")
                return

            if trigger.is_privmsg:
                bot.notice("This command must be run in a channel you which to enable it in.", trigger.nick)
                return

            disabled_list = spicedb.get_channel_value(bot, trigger.sender, 'disabled_commands', 'commands') or {}

            if argsdict["realcom"] not in disabled_list.keys():
                bot.notice(argsdict["com"] + " is already enabled in " + str(trigger.sender), trigger.nick)
                return

            del disabled_list[argsdict["realcom"]]
            spicedb.set_channel_value(bot, trigger.sender, 'disabled_commands', disabled_list, 'commands')
            bot.say(argsdict["com"] + " is now enabled in " + str(trigger.sender))
            return

        elif hyphenarg in ['disable']:

            if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
                bot.say("I was unable to disable this command due to privilege issues.")
                return

            if trigger.is_privmsg:
                bot.notice("This command must be run in a channel you which to disable it in.", trigger.nick)
                return

            disabled_list = spicedb.get_channel_value(bot, trigger.sender, 'disabled_commands', 'commands') or {}

            if argsdict["realcom"] in disabled_list.keys():
                bot.notice(argsdict["com"] + " is already disabled in " + str(trigger.sender), trigger.nick)
                return

            trailingmessage = spicemanip.main(argsdict["args"], 0) or "No reason given."
            timestamp = str(datetime.datetime.utcnow())

            disabled_list[argsdict["realcom"]] = {"reason": trailingmessage, "timestamp": timestamp, "disabledby": trigger.nick}
            spicedb.set_channel_value(bot, trigger.sender, 'disabled_commands', disabled_list, 'commands')

            spicedb.adjust_channel_list(bot, trigger.sender, 'disabled_commands', argsdict["realcom"], 'add', 'commands')
            bot.say(argsdict["com"] + " is now disabled in " + str(trigger.sender))
            return

        return

    def runstatus(self, bot, trigger, argsdict):

        # Hyphen args can only be used one per && split
        if len(argsdict["hyphen_args"]):
            return False

        # don't run commands that are disabled in channels
        if not trigger.is_privmsg:
            disabled_list = spicedb.get_channel_value(bot, trigger.sender, 'disabled_commands', 'commands') or {}
            if argsdict["realcom"] in disabled_list.keys():
                reason = disabled_list[argsdict["realcom"]]["reason"]
                timestamp = disabled_list[argsdict["realcom"]]["timestamp"]
                bywhom = disabled_list[argsdict["realcom"]]["disabledby"]
                bot.notice("The " + str(argsdict["com"]) + " command was disabled by " + bywhom + " in " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason), trigger.nick)
                return False

        return True


prerun = BotPrerun()
