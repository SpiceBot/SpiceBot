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

from .Tools import command_permissions_check, class_create
from .Commands import commands as botcommands
from .Database import db as botdb
from .Channels import channels as botchannels
from .MessageLog import messagelog as botmessagelog
from .Config import config as botconfig
from .Users import users as botusers


def prerun(t_command_type='module', t_command_subtype=None):

    def actual_decorator(function):

        @functools.wraps(function)
        def internal_prerun(bot, trigger, *args, **kwargs):

            botcom = class_create('botcom')

            if t_command_type == "nickname":
                check_nick = spicemanip.main(trigger.args[1], 1).lower()
                if check_nick != str(bot.nick).lower():
                    return
            else:
                if not str(trigger.args[1]).startswith(tuple(botconfig.core.prefix_list)):
                    return

            trigger_command_type = str(t_command_type)

            # Primary command used for trigger, and a list of all words
            trigger_args, trigger_command, trigger_prefix = make_trigger_args(trigger.args[1], trigger_command_type)

            if trigger_prefix == botconfig.SpiceBot_Commands.query_prefix:
                return

            trigger_command_type = botcommands.find_command_type(trigger_command)
            if not trigger_command_type:
                return

            if t_command_subtype:
                if trigger_command_type != t_command_subtype:
                    return

            # Argsdict Defaults
            argsdict_default = {}
            argsdict_default["type"] = trigger_command_type
            argsdict_default["com"] = trigger_command

            # messagelog ID
            argsdict_default["log_id"] = botmessagelog.messagelog_assign()

            argsdict_default["realcom"] = botcommands.get_realcom(argsdict_default["com"], trigger_command_type)

            if argsdict_default["type"] == 'nickname':
                argsdict_default["comtext"] = "'" + bot.nick + " " + argsdict_default["com"] + "'"
                argsdict_default["realcomtext"] = "'" + bot.nick + " " + argsdict_default["realcom"] + "'"
            else:
                argsdict_default["comtext"] = "'" + argsdict_default["com"] + "'"
                argsdict_default["realcomtext"] = "'" + argsdict_default["realcom"] + "'"

            argsdict_default["realcomref"] = argsdict_default["type"] + "_" + argsdict_default["realcom"]

            argsdict_default["dict"] = botcommands.get_command_dict(argsdict_default["realcom"], trigger_command_type)

            # split into && groupings
            and_split = trigger_and_split(trigger_args)

            # Create dict listings for trigger.sb
            argsdict_list = trigger_argsdict_list(argsdict_default, and_split)

            # Run the function for all splits
            botmessagelog.messagelog_start(bot, trigger, argsdict_default["log_id"], argsdict_default["realcomtext"])
            runcount = 0
            for argsdict in argsdict_list:
                runcount += 1
                trigger.sb = copy.deepcopy(argsdict)

                trigger.sb["runcount"] = runcount

                trigger.sb["args"], trigger.sb["hyphen_arg"] = trigger_hyphen_args(trigger.sb["args"])
                if not trigger.sb["hyphen_arg"]:
                    # check if anything prohibits the nick from running the command
                    if trigger_runstatus(bot, trigger):
                        function(bot, trigger, botcom, *args, **kwargs)
                else:
                    trigger_hyphen_arg_handler(bot, trigger)
            botmessagelog.messagelog_exit(bot, argsdict_default["log_id"])

        return internal_prerun
    return actual_decorator


def prerun_query(t_command_type='module', t_command_subtype=None):

    def actual_decorator(function):

        @functools.wraps(function)
        def internal_prerun(bot, trigger, *args, **kwargs):

            botcom = class_create('botcom')

            if t_command_type == "nickname":
                check_nick = spicemanip.main(trigger.args[1], 1).lower()
                if check_nick != str(bot.nick).lower():
                    return
            else:
                if not str(trigger.args[1]).startswith(tuple(botconfig.core.prefix_list)):
                    return

            if t_command_subtype != t_command_type:
                return

            trigger_command_type = str(t_command_type)

            # Primary command used for trigger, and a list of all words
            trigger_args, trigger_command, trigger_prefix = make_trigger_args(trigger.args[1], trigger_command_type)

            if trigger_prefix != botconfig.SpiceBot_Commands.query_prefix:
                return

            # Argsdict Defaults
            argsdict_default = {}
            argsdict_default["type"] = trigger_command_type
            argsdict_default["com"] = trigger_command

            # messagelog ID
            argsdict_default["log_id"] = botmessagelog.messagelog_assign()

            argsdict_default["realcom"] = "query"

            argsdict_default["comtext"] = "'" + bot.nick + " query'"
            argsdict_default["realcomtext"] = "'" + bot.nick + " query'"

            argsdict_default["realcomref"] = "nickname_query"

            argsdict_default["dict"] = botcommands.get_command_dict("query", 'nickname')

            # Create dict listings for trigger.sb
            argsdict = trigger_argsdict_single(argsdict_default, trigger_args)

            # Run the function for all splits
            botmessagelog.messagelog_start(bot, trigger, argsdict_default["log_id"], argsdict_default["realcomtext"])

            trigger.sb = copy.deepcopy(argsdict)

            trigger.sb["runcount"] = 1

            # check if anything prohibits the nick from running the command
            if trigger_runstatus_query(bot, trigger):
                function(bot, trigger, botcom, *args, **kwargs)
            botmessagelog.messagelog_exit(bot, argsdict_default["log_id"])

        return internal_prerun
    return actual_decorator


def make_trigger_args(triggerargs_one, trigger_command_type='module'):
    trigger_args = spicemanip.main(triggerargs_one, 'create')
    if trigger_command_type in ['nickname']:
        trigger_prefix = spicemanip.main(trigger_args, 2).lower()[0]
        if trigger_prefix.isupper() or trigger_prefix.islower():
            trigger_prefix = None
        trigger_command = spicemanip.main(trigger_args, 2).lower()
        trigger_args = spicemanip.main(trigger_args, '3+', 'list')
    else:
        trigger_prefix = spicemanip.main(trigger_args, 1).lower()[0]
        trigger_command = spicemanip.main(trigger_args, 1).lower()[1:]
        trigger_args = spicemanip.main(trigger_args, '2+', 'list')
    return trigger_args, trigger_command, trigger_prefix


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
        if len(argsdict_part["args"]) and (argsdict_part["args"][0] == "-a" or argsdict_part["args"][-1] == "-a"):
            argsdict_part["adminswitch"] = True
            if argsdict_part["args"][0] == "-a":
                argsdict_part["args"] = spicemanip.main(argsdict_part["args"], '2+', 'list')
            elif argsdict_part["args"][-1] == "-a":
                del argsdict_part["args"][-1]
        else:
            argsdict_part["adminswitch"] = False
        prerun_split.append(argsdict_part)
    return prerun_split


def trigger_argsdict_single(argsdict_default, trigger_args_part):
    argsdict_part = copy.deepcopy(argsdict_default)
    argsdict_part["args"] = spicemanip.main(trigger_args_part, 'create')
    if len(argsdict_part["args"]) and (argsdict_part["args"][0] == "-a" or argsdict_part["args"][-1] == "-a"):
        argsdict_part["adminswitch"] = True
        if argsdict_part["args"][0] == "-a":
            argsdict_part["args"] = spicemanip.main(argsdict_part["args"], '2+', 'list')
        elif argsdict_part["args"][-1] == "-a":
            del argsdict_part["args"][-1]
    else:
        argsdict_part["adminswitch"] = False
    return argsdict_part


def trigger_runstatus_query(bot, trigger):

    # Bots can't run commands
    if Identifier(trigger.nick) == bot.nick:
        return False

    # Allow permissions for enabling and disabling commands via hyphenargs
    if trigger.sb["adminswitch"]:
        if command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            return True
        else:
            botmessagelog.messagelog_error(trigger.sb["log_id"], "The admin switch (-a) is for use by authorized nicks ONLY.")
            return False

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender), "fully")
        if "nickname_query" in list(channel_disabled_list.keys()):
            return False

    # don't run commands that are disabled for specific users
    nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick), "fully")
    if "nickname_query" in list(nick_disabled_list.keys()):
        return False

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender), "fully")
        if trigger.sb["realcomref"] in list(channel_disabled_list.keys()):
            reason = channel_disabled_list[trigger.sb["realcomref"]]["reason"]
            timestamp = channel_disabled_list[trigger.sb["realcomref"]]["timestamp"]
            bywhom = channel_disabled_list[trigger.sb["realcomref"]]["disabledby"]
            message = "The " + str(trigger.sb["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, message)

    # don't run commands that are disabled for specific users
    nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick), "fully")
    if trigger.sb["realcomref"] in list(nick_disabled_list.keys()):
        bywhom = nick_disabled_list[trigger.sb["realcomref"]]["disabledby"]
        if botusers.ID(bywhom) != botusers.ID(trigger.nick):
            reason = nick_disabled_list[trigger.sb["realcomref"]]["reason"]
            timestamp = nick_disabled_list[trigger.sb["realcomref"]]["timestamp"]
            message = "The " + str(trigger.sb["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, message)
        else:
            botcommands.unset_command_disabled(trigger.sb["realcomref"], trigger.nick, "fully")
            botmessagelog.messagelog_error(trigger.sb["log_id"], trigger.sb["comtext"] + " is now enabled for " + str(trigger.nick))

    return True


def trigger_runstatus(bot, trigger):

    # Bots can't run commands
    if Identifier(trigger.nick) == bot.nick:
        return False

    # Allow permissions for enabling and disabling commands via hyphenargs
    if trigger.sb["adminswitch"]:
        if command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            return True
        else:
            botmessagelog.messagelog_error(trigger.sb["log_id"], "The admin switch (-a) is for use by authorized nicks ONLY.")
            return False

    if trigger.sb["hyphen_arg"]:
        return False

    if trigger.sb["runcount"] > 1:
        # check channel multirun blocks
        if not trigger.is_privmsg:
            channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender), "multirun")
            if trigger.sb["realcomref"] in list(channel_disabled_list.keys()):
                reason = channel_disabled_list[trigger.sb["realcomref"]]["reason"]
                timestamp = channel_disabled_list[trigger.sb["realcomref"]]["timestamp"]
                bywhom = channel_disabled_list[trigger.sb["realcomref"]]["disabledby"]
                message = "The " + str(trigger.sb["comtext"]) + " command multirun usage was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
                return trigger_cant_run(bot, trigger, message)

        # don't run commands that are disabled for specific users
        nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick), "multirun")
        if trigger.sb["realcomref"] in list(nick_disabled_list.keys()):
            bywhom = nick_disabled_list[trigger.sb["realcomref"]]["disabledby"]
            if botusers.ID(bywhom) != botusers.ID(trigger.nick):
                reason = nick_disabled_list[trigger.sb["realcomref"]]["reason"]
                timestamp = nick_disabled_list[trigger.sb["realcomref"]]["timestamp"]
                message = "The " + str(trigger.sb["comtext"]) + " command was multirun unsage disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
                return trigger_cant_run(bot, trigger, message)
            else:
                botcommands.unset_command_disabled(trigger.sb["realcomref"], trigger.nick, "multirun")
                botmessagelog.messagelog_error(trigger.sb["log_id"], trigger.sb["comtext"] + " multirun is now enabled for " + str(trigger.nick))

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender), "fully")
        if trigger.sb["realcomref"] in list(channel_disabled_list.keys()):
            reason = channel_disabled_list[trigger.sb["realcomref"]]["reason"]
            timestamp = channel_disabled_list[trigger.sb["realcomref"]]["timestamp"]
            bywhom = channel_disabled_list[trigger.sb["realcomref"]]["disabledby"]
            message = "The " + str(trigger.sb["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, message)

    # don't run commands that are disabled for specific users
    nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick), "fully")
    if trigger.sb["realcomref"] in list(nick_disabled_list.keys()):
        bywhom = nick_disabled_list[trigger.sb["realcomref"]]["disabledby"]
        if botusers.ID(bywhom) != botusers.ID(trigger.nick):
            reason = nick_disabled_list[trigger.sb["realcomref"]]["reason"]
            timestamp = nick_disabled_list[trigger.sb["realcomref"]]["timestamp"]
            message = "The " + str(trigger.sb["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, message)
        else:
            botcommands.unset_command_disabled(trigger.sb["realcomref"], trigger.nick, "fully")
            botmessagelog.messagelog_error(trigger.sb["log_id"], trigger.sb["comtext"] + " is now enabled for " + str(trigger.nick))

    return True


def trigger_cant_run(bot, trigger, message=None):
    if message:
        botmessagelog.messagelog_error(trigger.sb["log_id"], message)
    if command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        botmessagelog.messagelog_error(trigger.sb["log_id"], "You however are authorized to bypass this warning with the (-a) admin switch.")
    return False


def trigger_hyphen_args(trigger_args_part):
    valid_hyphen_args = [
                        'check',
                        'enable', 'disable',
                        'block', 'unblock',
                        "activate", "deactivate",
                        "on", "off",
                        'multirun', 'multiruns',
                        'example', 'usage',
                        'filename', 'filepath',
                        'foldername', 'folderpath',
                        "author",
                        'contribs', 'contrib', "contributors",
                        'alias', 'aliases'
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
            botmessagelog.messagelog(trigger.sb["log_id"], trigger.sb["comtext"] + " is a valid alias command for " + trigger.sb["realcomtext"])
        else:
            botmessagelog.messagelog(trigger.sb["log_id"], trigger.sb["comtext"] + " is a valid command")
        return

    elif trigger.sb["hyphen_arg"] in [
                                        'enable', 'disable',
                                        'block', 'unblock',
                                        "activate", "deactivate",
                                        "on", "off"
                                        ]:

        target = spicemanip.main(trigger.sb["args"], 1) or trigger.nick
        if not target:
            if trigger.sb["hyphen_arg"] in ['enable', 'unblock', "activate", "on"]:
                botmessagelog.messagelog_error(trigger.sb["log_id"], "Who/Where am I enabling " + str(trigger.sb["comtext"]) + " usage for?")
            else:
                botmessagelog.messagelog_error(trigger.sb["log_id"], "Who/Where am I disabling " + str(trigger.sb["comtext"]) + " usage for?")
            return
        trigger.sb["args"] = spicemanip.main(trigger.sb["args"], "2+", "list")

        if not botdb.check_nick_id(target) and not botchannels.check_channel_bot(target, True):
            botmessagelog.messagelog_error(trigger.sb["log_id"], "I don't know who/what " + str(target) + " is.")
            return

        if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            if target != trigger.nick:
                if trigger.sb["hyphen_arg"] in ['enable', 'unblock', "activate", "on"]:
                    botmessagelog.messagelog_error(trigger.sb["log_id"], "I was unable to enable this command for " + str(target) + " due to privilege issues.")
                else:
                    botmessagelog.messagelog_error(trigger.sb["log_id"], "I was unable to disable this command for " + str(target) + " due to privilege issues.")
                return

        if trigger.sb["hyphen_arg"] in ['enable', 'unblock', "activate", "on"]:

            if not botcommands.check_commands_disabled(trigger.sb["realcomref"], target, "fully"):
                botmessagelog.messagelog_error(trigger.sb["log_id"], trigger.sb["comtext"] + " is already enabled for " + str(target))
                return

            botcommands.unset_command_disabled(trigger.sb["realcomref"], target, "fully")
            botmessagelog.messagelog(trigger.sb["log_id"], trigger.sb["comtext"] + " is now enabled for " + str(target))
            return

        else:

            if botcommands.check_commands_disabled(trigger.sb["realcomref"], target, "fully"):
                botmessagelog.messagelog_error(trigger.sb["log_id"], trigger.sb["comtext"] + " is already disabled for " + str(target))
                return

            trailingmessage = spicemanip.main(trigger.sb["args"], 0) or "No reason given."
            timestamp = str(datetime.datetime.utcnow())

            botcommands.set_command_disabled(trigger.sb["realcomref"], target, timestamp, trailingmessage, trigger.nick, "fully")
            botmessagelog.messagelog(trigger.sb["log_id"], trigger.sb["comtext"] + " is now disabled for " + str(target))
            return

    if trigger.sb["hyphen_arg"] in ['multirun', 'multiruns']:

        onoff = spicemanip.main(trigger.sb["args"], 1) or None
        if not onoff or onoff not in ['enable', 'unblock', "activate", "on"]:
            botmessagelog.messagelog_error(trigger.sb["log_id"], "Do you want to enable or disable " + str(trigger.sb["comtext"]) + " multirun usage?")
            return

        target = spicemanip.main(trigger.sb["args"], 1) or trigger.nick
        if not target:
            if onoff in ['enable', 'unblock', "activate", "on"]:
                botmessagelog.messagelog_error(trigger.sb["log_id"], "Who/Where am I enabling " + str(trigger.sb["comtext"]) + " multirun usage for?")
            else:
                botmessagelog.messagelog_error(trigger.sb["log_id"], "Who/Where am I disabling " + str(trigger.sb["comtext"]) + " multirun usage for?")
            return
        trigger.sb["args"] = spicemanip.main(trigger.sb["args"], "2+", "list")

        if not botdb.check_nick_id(target) and not botchannels.check_channel_bot(target, True):
            botmessagelog.messagelog_error(trigger.sb["log_id"], "I don't know who/what " + str(target) + " is.")
            return

        if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            if target != trigger.nick:
                if onoff in ['enable', 'unblock', "activate", "on"]:
                    botmessagelog.messagelog_error(trigger.sb["log_id"], "I was unable to enable multirun usage on " + str(trigger.sb["comtext"]) + " for " + str(target) + " due to privilege issues.")
                else:
                    botmessagelog.messagelog_error(trigger.sb["log_id"], "I was unable to enable multirun usage on " + str(trigger.sb["comtext"]) + " for " + str(target) + " due to privilege issues.")
                return

        if onoff in ['enable', 'unblock', "activate", "on"]:

            if not botcommands.check_commands_disabled(trigger.sb["realcomref"], target, "multirun"):
                botmessagelog.messagelog_error(trigger.sb["log_id"], trigger.sb["comtext"] + " multirun is already enabled for " + str(target))
                return

            botcommands.unset_command_disabled(trigger.sb["realcomref"], target, "multirun")
            botmessagelog.messagelog(trigger.sb["log_id"], trigger.sb["comtext"] + " multirun is now enabled for " + str(target))
            return

        else:

            if botcommands.check_commands_disabled(trigger.sb["realcomref"], target, "multirun"):
                botmessagelog.messagelog_error(trigger.sb["log_id"], trigger.sb["comtext"] + " multirun is already disabled for " + str(target))
                return

            trailingmessage = spicemanip.main(trigger.sb["args"], 0) or "No reason given."
            timestamp = str(datetime.datetime.utcnow())

            botcommands.set_command_disabled(trigger.sb["realcomref"], target, timestamp, trailingmessage, trigger.nick, "multirun")
            botmessagelog.messagelog(trigger.sb["log_id"], trigger.sb["comtext"] + " multirun is now disabled for " + str(target))
            return

    elif trigger.sb["hyphen_arg"] in ['example', 'usage']:
        botmessagelog.messagelog(trigger.sb["log_id"], trigger.sb["comtext"] + ": " + str(trigger.sb["dict"]["example"]))
        return

    elif trigger.sb["hyphen_arg"] in ['filename', 'filepath']:
        botmessagelog.messagelog(trigger.sb["log_id"], "The " + str(trigger.sb["comtext"]) + " file is located at " + str(trigger.sb["dict"][trigger.sb["hyphen_arg"]]))
        return

    elif trigger.sb["hyphen_arg"] in ['foldername', 'folderpath']:
        botmessagelog.messagelog(trigger.sb["log_id"], "The " + str(trigger.sb["comtext"]) + " folder is located at " + str(trigger.sb["dict"][trigger.sb["hyphen_arg"]]))
        return

    elif trigger.sb["hyphen_arg"] in ['author']:
        botmessagelog.messagelog(trigger.sb["log_id"], "The author of the " + str(trigger.sb["comtext"]) + " command is " + trigger.sb["dict"]["author"] + ".")
        return

    elif trigger.sb["hyphen_arg"] in ['contribs', 'contrib', "contributors"]:
        botmessagelog.messagelog(trigger.sb["log_id"], "The contributors of the " + str(trigger.sb["comtext"]) + " command are " + spicemanip.main(trigger.sb["dict"]["contributors"], "andlist") + ".")
        return

    elif trigger.sb["hyphen_arg"] in ['alias', 'aliases']:
        botmessagelog.messagelog(trigger.sb["log_id"], "The alaises of the " + str(trigger.sb["comtext"]) + " command are " + spicemanip.main(trigger.sb["dict"]["validcoms"], "andlist") + ".")
        return

    return
