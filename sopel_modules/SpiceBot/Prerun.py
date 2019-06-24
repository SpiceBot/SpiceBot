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
from .Commands import commands as botcommands
from .Database import db as botdb


def prerun_old(trigger_command_type='module'):
    def actual_decorator(function):

        @functools.wraps(function)
        def internal_prerun(*args, **kwargs):

            # Assign trigger and bot for easy access later
            bot, trigger = args[0:2]

            # Primary command used for trigger, and a list of all words
            trigger_args, trigger_command = make_trigger_args(trigger.args[1], trigger_command_type)

            # Argsdict Defaults
            argsdict_default = {}
            argsdict_default["type"] = trigger_command_type
            argsdict_default["com"] = trigger_command

            realcom = botcommands.get_realcom(argsdict_default["com"], trigger_command_type)
            argsdict_default["realcom"] = realcom

            # split into && groupings
            # and_split = trigger_and_split(trigger_args)

            # Create dict listings for trigger.sb
            # argsdict_list = trigger_argsdict_list(argsdict_default, and_split)
            argsdict = trigger_argsdict_single(argsdict_default, trigger_args)

            trigger.sb = copy.deepcopy(argsdict)

            trigger.sb["args"], trigger.sb["hyphen_arg"] = trigger_hyphen_args(trigger.sb["args"])
            if not trigger.sb["hyphen_arg"]:
                # check if anything prohibits the nick from running the command
                if trigger_runstatus(bot, trigger):
                    return function(bot, trigger, *args, **kwargs)
            else:
                return trigger_hyphen_arg_handler(bot, trigger)

            """# Run the function for all splits
            for argsdict in argsdict_list:
                trigger.sb = copy.deepcopy(argsdict)

                trigger.sb["args"], trigger.sb["hyphen_arg"] = trigger_hyphen_args(trigger.sb["args"])
                if not trigger.sb["hyphen_arg"]:
                    # check if anything prohibits the nick from running the command
                    if trigger_runstatus(bot, trigger):
                        function(bot, trigger, *args, **kwargs)
                else:
                    trigger_hyphen_arg_handler(bot, trigger)
            """
        return internal_prerun
    return actual_decorator


def prerun(message="this is not privmsg", reply=False):

    def actual_decorator(function):
        @functools.wraps(function)
        def _nop(*args, **kwargs):
            # Assign trigger and bot for easy access later
            bot, trigger = args[0:2]
            if not trigger.is_privmsg:
                if message and not callable(message):
                    if reply:
                        bot.reply(message)
                    else:
                        bot.say(message)
            else:
                return function(*args, **kwargs)
        return _nop

    # Hack to allow decorator without parens
    if callable(message):
        return actual_decorator(message)
    return actual_decorator


def make_trigger_args(triggerargs_one, trigger_command_type='module'):
    trigger_args = spicemanip.main(triggerargs_one, 'create')
    if trigger_command_type in ['nickname']:
        trigger_command = spicemanip.main(trigger_args, 2).lower()
        trigger_args = spicemanip.main(trigger_args, '3+', 'list')
    else:
        trigger_command = spicemanip.main(trigger_args, 1).lower()[1:]
        trigger_args = spicemanip.main(trigger_args, '2+', 'list')
    return trigger_args, trigger_command


def trigger_and_split(trigger_args):
    trigger_args_list_split = spicemanip.main(trigger_args, "split_&&")
    if not len(trigger_args_list_split):
        trigger_args_list_split.append([])
    return trigger_args_list_split


def trigger_argsdict_list(argsdict_default, and_split):
    prerun_split = []
    for trigger_args_part in and_split:
        argsdict_part = copy.deepcopy(argsdict_default)
        argsdict_part["args"] = spicemanip.main(trigger_args_part, 'create')
        if len(argsdict_part["args"]) and argsdict_part["args"][0] == "-a":
            argsdict_part["adminswitch"] = True
            argsdict_part["args"] = spicemanip.main(argsdict_part["args"], '2+', 'list')
        else:
            argsdict_part["adminswitch"] = False
        prerun_split.append(argsdict_part)
    return prerun_split


def trigger_argsdict_single(argsdict_default, trigger_args_part):
    argsdict_part = copy.deepcopy(argsdict_default)
    argsdict_part["args"] = spicemanip.main(trigger_args_part, 'create')
    if len(argsdict_part["args"]) and argsdict_part["args"][0] == "-a":
        argsdict_part["adminswitch"] = True
        argsdict_part["args"] = spicemanip.main(argsdict_part["args"], '2+', 'list')
    else:
        argsdict_part["adminswitch"] = False
    return argsdict_part


def trigger_runstatus(bot, trigger):

    # Bots can't run commands
    if Identifier(trigger.nick) == bot.nick:
        return False

    # Allow permissions for enabling and disabling commands via hyphenargs
    if trigger.sb["adminswitch"]:
        if command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            return True
        else:
            bot.osd("The admin switch (-a) is for use by authorized nicks ONLY.", 'notice')
            return False

    if trigger.sb["hyphen_arg"]:
        return False

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        commandused = trigger.sb["realcom"]
        disabled_list = botdb.get_channel_value(trigger.sender, 'commands_disabled') or {}
        if commandused in list(disabled_list.keys()):
            reason = disabled_list[trigger.sb["realcom"]]["reason"]
            timestamp = disabled_list[trigger.sb["realcom"]]["timestamp"]
            bywhom = disabled_list[trigger.sb["realcom"]]["disabledby"]
            message = "The " + str(trigger.sb["com"]) + " command was disabled by " + bywhom + " in " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, message)

    return True


def trigger_cant_run(bot, trigger, message=None):
    if message:
        bot.osd(message, trigger.nick, 'notice')
    if command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.osd("You however are authorized to bypass this warning with the (-a) admin switch.", trigger.nick, 'notice')
    return False


def trigger_hyphen_args(trigger_args_part):
    valid_hyphen_args = [
                        'check',
                        'enable', 'disable'
                        ]
    hyphen_args = []
    trigger_args_unhyphend = []
    for worditem in trigger_args_part:
        if str(worditem).startswith("--") and worditem[2:] in valid_hyphen_args:
            hyphen_args.append(worditem[2:])
        else:
            trigger_args_unhyphend.append(worditem)
    if len(hyphen_args):
        hyphenarg = hyphen_args[0]
    else:
        hyphenarg = None
    return trigger_args_unhyphend, hyphenarg


def trigger_hyphen_arg_handler(bot, trigger):

    # Commands that cannot run via privmsg
    if trigger.sb["hyphen_arg"] in ['check']:
        if trigger.sb["com"].lower() != trigger.sb["realcom"]:
            bot.osd(trigger.sb["com"] + " is a valid alias command for " + trigger.sb["realcom"])
        else:
            bot.osd(trigger.sb["com"] + " is a valid command")
        return

    elif trigger.sb["hyphen_arg"] in ['enable']:

        if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            bot.osd("I was unable to disable this command due to privilege issues.")
            return

        if trigger.is_privmsg:
            bot.osd("This command must be run in a channel you which to enable it in.", trigger.nick, 'notice')
            return

        if not botcommands.check_commands_disabled(trigger.sb["realcom"], trigger.sender):
            bot.osd(trigger.sb["com"] + " is already enabled in " + str(trigger.sender), trigger.nick, 'notice')
            return

        botcommands.unset_command_disabled(trigger.sb["realcom"], trigger.sender)
        bot.osd(trigger.sb["com"] + " is now enabled in " + str(trigger.sender))
        return

    elif trigger.sb["hyphen_arg"] in ['disable']:

        if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            bot.osd("I was unable to disable this command due to privilege issues.")
            return

        if trigger.is_privmsg:
            bot.osd("This command must be run in a channel you which to disable it in.", trigger.nick, 'notice')
            return

        if botcommands.check_commands_disabled(trigger.sb["realcom"], trigger.sender):
            bot.osd(trigger.sb["com"] + " is already disabled in " + str(trigger.sender), trigger.nick, 'notice')
            return

        trailingmessage = spicemanip.main(trigger.sb["args"], 0) or "No reason given."
        timestamp = str(datetime.datetime.utcnow())

        botcommands.set_command_disabled(trigger.sb["realcom"], trigger.sender, timestamp, trailingmessage, trigger.nick)
        bot.osd(trigger.sb["com"] + " is now disabled in " + str(trigger.sender))
        return

    return
