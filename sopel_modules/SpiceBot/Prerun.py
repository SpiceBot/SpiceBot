# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Prerun system.
"""

from sopel.tools import Identifier

import functools
import copy
import datetime
from word2number import w2n

from sopel_modules.spicemanip import spicemanip

from .Tools import class_create
from .Commands import commands as botcommands
from .Database import db as botdb
from .Channels import channels as botchannels
from .MessageLog import messagelog as botmessagelog
from .Config import config as botconfig
from .Users import users as botusers
from .Events import events as botevents
from .Tools import prerun_shared


def prerun(t_command_type='module', t_command_subtype=None):

    def actual_decorator(function):

        @functools.wraps(function)
        def internal_prerun(bot, trigger, *args, **kwargs):

            # verify the bot is at a loaded state
            while not botevents.check(botevents.BOT_LOADED):
                pass

            # Verify channel and user exist
            verify_channel(trigger)
            verify_user(bot, trigger)

            botcom = class_create('botcom')

            if t_command_type == "nickname":
                check_nick = spicemanip(trigger.args[1], 1).lower()
                if check_nick != str(bot.nick).lower():
                    return
            elif t_command_type == "module":
                if not str(trigger.args[1]).startswith(tuple(botconfig.core.prefix_list)):
                    return

            trigger_command_type = str(t_command_type)

            # Primary command used for trigger, and a list of all words
            trigger_args, trigger_command, trigger_prefix = make_trigger_args(trigger.args[1], trigger_command_type)

            if trigger_prefix and trigger_prefix in [botconfig.SpiceBot_Commands.query_prefix]:
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
            argsdict_default["trigger_prefix"] = trigger_prefix

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

            # Create dict listings for botcom.dict
            argsdict_list = trigger_argsdict_list(argsdict_default, and_split)

            # Run the function for all splits
            botmessagelog.messagelog_start(bot, trigger, argsdict_default["log_id"], argsdict_default["realcomtext"])
            runcount = 0
            for argsdict in argsdict_list:
                runcount += 1
                botcom.dict = copy.deepcopy(argsdict)

                botcom.dict["runcount"] = runcount

                botcom.dict["args"], botcom.dict["hyphen_arg"] = trigger_hyphen_args(botcom)

                # special handling
                botcom = special_handling(botcom)

                args_pass = trigger_hyphen_arg_handler(bot, trigger, botcom)

                if args_pass:

                    if trigger_runstatus(bot, trigger, botcom):
                        function(bot, trigger, botcom, *args, **kwargs)
            botmessagelog.messagelog_exit(bot, argsdict_default["log_id"])

        return internal_prerun
    return actual_decorator


def prerun_query(t_command_type='module', t_command_subtype=None):

    def actual_decorator(function):

        @functools.wraps(function)
        def internal_prerun(bot, trigger, *args, **kwargs):

            # verify the bot is at a loaded state
            while not botevents.check(botevents.BOT_LOADED):
                pass

            # Verify channel and user exist
            verify_channel(trigger)
            verify_user(bot, trigger)

            botcom = class_create('botcom')

            if t_command_type == "nickname":
                check_nick = spicemanip(trigger.args[1], 1).lower()
                if check_nick != str(bot.nick).lower():
                    return
            elif t_command_type == "module":
                if not str(trigger.args[1]).startswith(tuple(botconfig.core.prefix_list)):
                    return

            if t_command_subtype != t_command_type:
                return

            trigger_command_type = str(t_command_type)

            # Primary command used for trigger, and a list of all words
            trigger_args, trigger_command, trigger_prefix = make_trigger_args(trigger.args[1], trigger_command_type)

            if trigger_prefix and trigger_prefix not in [botconfig.SpiceBot_Commands.query_prefix]:
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

            # Create dict listings for botcom.dict
            argsdict = trigger_argsdict_single(argsdict_default, trigger_args)

            # Run the function for all splits
            botmessagelog.messagelog_start(bot, trigger, argsdict_default["log_id"], argsdict_default["realcomtext"])

            botcom.dict = copy.deepcopy(argsdict)

            botcom.dict["runcount"] = 1

            # check if anything prohibits the nick from running the command
            if trigger_runstatus_query(bot, trigger, botcom):
                function(bot, trigger, botcom, *args, **kwargs)
            botmessagelog.messagelog_exit(bot, argsdict_default["log_id"])

        return internal_prerun
    return actual_decorator


def verify_user(bot, trigger):
    # Identify
    nick_id = botusers.whois_ident(trigger.nick)
    # check if nick is registered
    botusers.whois_send(bot, trigger.nick)
    # Verify nick is in the all list
    botusers.add_to_all(trigger.nick, nick_id)
    # Verify nick is in the all list
    botusers.add_to_current(trigger.nick, nick_id)
    # set current nick
    botusers.mark_current_nick(trigger.nick, nick_id)
    # add joined channel to nick list
    botusers.add_channel(trigger.sender, nick_id)
    # mark user as online
    botusers.mark_user_online(nick_id)


def verify_channel(trigger):
    botchannels.add_channel(trigger.sender)
    # Identify
    nick_id = botchannels.whois_ident(trigger.nick)
    # Verify nick is in the channel list
    botchannels.add_to_channel(trigger.sender, trigger.nick, nick_id)


def make_trigger_args(triggerargs_one, trigger_command_type='module'):
    trigger_args = spicemanip(triggerargs_one, 'create')
    if trigger_command_type in ['nickname']:
        trigger_prefix = None
        # if trigger_prefix.isupper() or trigger_prefix.islower():
        #    trigger_prefix = None
        trigger_command = spicemanip(trigger_args, 2).lower()
        trigger_args = spicemanip(trigger_args, '3+', 'list')
    elif trigger_command_type in ['action']:
        trigger_prefix = None
        trigger_command = spicemanip(trigger_args, 1).lower()
        trigger_args = spicemanip(trigger_args, '2+', 'list')
    else:
        trigger_prefix = spicemanip(trigger_args, 1).lower()[0]
        trigger_command = spicemanip(trigger_args, 1).lower()[1:]
        trigger_args = spicemanip(trigger_args, '2+', 'list')
    return trigger_args, trigger_command, trigger_prefix


def trigger_and_split(trigger_args):
    trigger_args_list_split = spicemanip(trigger_args, "split_&&")
    if not len(trigger_args_list_split):
        trigger_args_list_split.append([])
    return trigger_args_list_split


def trigger_argsdict_list(argsdict_default, and_split):
    prerun_split = []
    for trigger_args_part in and_split:
        argsdict_part = copy.deepcopy(argsdict_default)
        argsdict_part["args"] = spicemanip(trigger_args_part, 'create')
        if len(argsdict_part["args"]) and (argsdict_part["args"][0] == "-a" or argsdict_part["args"][-1] == "-a"):
            argsdict_part["adminswitch"] = True
            if argsdict_part["args"][0] == "-a":
                argsdict_part["args"] = spicemanip(argsdict_part["args"], '2+', 'list')
            elif argsdict_part["args"][-1] == "-a":
                del argsdict_part["args"][-1]
        else:
            argsdict_part["adminswitch"] = False
        prerun_split.append(argsdict_part)
    return prerun_split


def trigger_argsdict_single(argsdict_default, trigger_args_part):
    argsdict_part = copy.deepcopy(argsdict_default)
    argsdict_part["args"] = spicemanip(trigger_args_part, 'create')
    if len(argsdict_part["args"]) and (argsdict_part["args"][0] == "-a" or argsdict_part["args"][-1] == "-a"):
        argsdict_part["adminswitch"] = True
        if argsdict_part["args"][0] == "-a":
            argsdict_part["args"] = spicemanip(argsdict_part["args"], '2+', 'list')
        elif argsdict_part["args"][-1] == "-a":
            del argsdict_part["args"][-1]
    else:
        argsdict_part["adminswitch"] = False
    return argsdict_part


def trigger_runstatus_query(bot, trigger, botcom):

    # Bots can't run commands
    if trigger.nick == bot.nick:
        return False

    # Allow permissions for enabling and disabling commands via hyphenargs
    if botcom.dict["adminswitch"]:
        if botusers.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            return True
        else:
            botmessagelog.messagelog_error(botcom.dict["log_id"], "The admin switch (-a) is for use by authorized nicks ONLY.")
            return False

    # Stop here if not registered or not identified
    if bot.config.SpiceBot_regnick.regnick:

        # not registered
        if str(trigger.nick).lower() not in [x.lower() for x in botusers.dict["registered"]]:
            message = "The " + str(botcom.dict["comtext"]) + " command requires you to be registered with IRC services. Registering may take a few minutes to process with the bot."
            return trigger_cant_run(bot, trigger, botcom, message)

        # registered nick, but not identified
        else:
            nick_id = botusers.whois_ident(trigger.nick)
            if nick_id not in botusers.dict["identified"]:
                message = "Your nickname appears to be registered with IRC services. However, you have not identified. Identifying may take a few minutes to process with the bot."
                return trigger_cant_run(bot, trigger, botcom, message)

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender))
        if "nickname_query" in list(channel_disabled_list.keys()):
            return False

    # don't run commands that are disabled for specific users
    nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick))
    if "nickname_query" in list(nick_disabled_list.keys()):
        return False

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender))
        if botcom.dict["realcomref"] in list(channel_disabled_list.keys()):
            reason = channel_disabled_list[botcom.dict["realcomref"]]["reason"]
            timestamp = channel_disabled_list[botcom.dict["realcomref"]]["timestamp"]
            bywhom = channel_disabled_list[botcom.dict["realcomref"]]["disabledby"]
            message = "The " + str(botcom.dict["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, botcom, message)

    # don't run commands that are disabled for specific users
    nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick))
    if botcom.dict["realcomref"] in list(nick_disabled_list.keys()):
        bywhom = nick_disabled_list[botcom.dict["realcomref"]]["disabledby"]
        if botusers.ID(bywhom) != botusers.ID(trigger.nick):
            reason = nick_disabled_list[botcom.dict["realcomref"]]["reason"]
            timestamp = nick_disabled_list[botcom.dict["realcomref"]]["timestamp"]
            message = "The " + str(botcom.dict["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, botcom, message)
        else:
            botcommands.unset_command_disabled(botcom.dict["realcomref"], trigger.nick)
            botmessagelog.messagelog_error(botcom.dict["log_id"], botcom.dict["comtext"] + " is now enabled for " + str(trigger.nick))

    return True


def trigger_runstatus(bot, trigger, botcom):

    # Bots can't run commands
    if Identifier(trigger.nick) == bot.nick:
        return False

    # Allow permissions for enabling and disabling commands via hyphenargs
    if botcom.dict["adminswitch"]:
        if botusers.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            return True
        else:
            botmessagelog.messagelog_error(botcom.dict["log_id"], "The admin switch (-a) is for use by authorized nicks ONLY.")
            return False

    # Stop here if not registered or not identified
    if bot.config.SpiceBot_regnick.regnick:

        # not registered
        if str(trigger.nick).lower() not in [x.lower() for x in botusers.dict["registered"]]:
            message = "The " + str(botcom.dict["comtext"]) + " command requires you to be registered with IRC services. Registering may take a few minutes to process with the bot."
            return trigger_cant_run(bot, trigger, botcom, message)

        # registered nick, but not identified
        else:
            nick_id = botusers.whois_ident(trigger.nick)
            if nick_id not in botusers.dict["identified"]:
                message = "Your nickname appears to be registered with IRC services. However, you have not identified. Identifying may take a few minutes to process with the bot."
                return trigger_cant_run(bot, trigger, botcom, message)

    # if botcom.dict["hyphen_arg"]:
    #    return False

    if not trigger.is_privmsg:
        if str(trigger.sender).lower() in [x.lower() for x in botcom.dict["dict"]["hardcoded_channel_block"]]:
            message = "The " + str(botcom.dict["comtext"]) + " command cannot be used in " + str(trigger.sender) + " because it is hardcoded not to."
            return trigger_cant_run(bot, trigger, botcom, message)

    if botcom.dict["runcount"] > 1:
        # check channel multirun blocks
        if not trigger.is_privmsg:
            channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender), "multirun")
            if botcom.dict["realcomref"] in list(channel_disabled_list.keys()):
                reason = channel_disabled_list[botcom.dict["realcomref"]]["reason"]
                timestamp = channel_disabled_list[botcom.dict["realcomref"]]["timestamp"]
                bywhom = channel_disabled_list[botcom.dict["realcomref"]]["disabledby"]
                message = "The " + str(botcom.dict["comtext"]) + " command multirun usage was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
                return trigger_cant_run(bot, trigger, botcom, message)

        # don't run commands that are disabled for specific users
        nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick), "multirun")
        if botcom.dict["realcomref"] in list(nick_disabled_list.keys()):
            bywhom = nick_disabled_list[botcom.dict["realcomref"]]["disabledby"]
            if botusers.ID(bywhom) != botusers.ID(trigger.nick):
                reason = nick_disabled_list[botcom.dict["realcomref"]]["reason"]
                timestamp = nick_disabled_list[botcom.dict["realcomref"]]["timestamp"]
                message = "The " + str(botcom.dict["comtext"]) + " command was multirun unsage disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
                return trigger_cant_run(bot, trigger, botcom, message)
            else:
                botcommands.unset_command_disabled(botcom.dict["realcomref"], trigger.nick, "multirun")
                botmessagelog.messagelog_error(botcom.dict["log_id"], botcom.dict["comtext"] + " multirun is now enabled for " + str(trigger.nick))

    # don't run commands that are disabled in channels
    if not trigger.is_privmsg:
        channel_disabled_list = botcommands.get_commands_disabled(str(trigger.sender))
        if botcom.dict["realcomref"] in list(channel_disabled_list.keys()):
            reason = channel_disabled_list[botcom.dict["realcomref"]]["reason"]
            timestamp = channel_disabled_list[botcom.dict["realcomref"]]["timestamp"]
            bywhom = channel_disabled_list[botcom.dict["realcomref"]]["disabledby"]
            message = "The " + str(botcom.dict["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, botcom, message)

    # don't run commands that are disabled for specific users
    nick_disabled_list = botcommands.get_commands_disabled(str(trigger.nick))
    if botcom.dict["realcomref"] in list(nick_disabled_list.keys()):
        bywhom = nick_disabled_list[botcom.dict["realcomref"]]["disabledby"]
        if botusers.ID(bywhom) != botusers.ID(trigger.nick):
            reason = nick_disabled_list[botcom.dict["realcomref"]]["reason"]
            timestamp = nick_disabled_list[botcom.dict["realcomref"]]["timestamp"]
            message = "The " + str(botcom.dict["comtext"]) + " command was disabled by " + bywhom + " for " + str(trigger.sender) + " at " + str(timestamp) + " for the following reason: " + str(reason)
            return trigger_cant_run(bot, trigger, botcom, message)
        else:
            botcommands.unset_command_disabled(botcom.dict["realcomref"], trigger.nick)
            botmessagelog.messagelog_error(botcom.dict["log_id"], botcom.dict["comtext"] + " is now enabled for " + str(trigger.nick))

    return True


def trigger_cant_run(bot, trigger, botcom, message=None):
    if message:
        botmessagelog.messagelog_error(botcom.dict["log_id"], message)
    if botusers.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        botmessagelog.messagelog_error(botcom.dict["log_id"], "You however are authorized to bypass this warning with the (-a) admin switch.")
    return False


def special_handling(botcom):
    botcom.dict["responsekey"] = "?default"

    # handling for special cases
    posscom = spicemanip(botcom.dict['args'], 1)
    if posscom.lower() in [command.lower() for command in botcom.dict["dict"]["nonstockoptions"]]:
        for command in botcom.dict["dict"]["nonstockoptions"]:
            if command.lower() == posscom.lower():
                posscom = command
        botcom.dict["responsekey"] = posscom

    if botcom.dict["responsekey"] != "?default":
        botcom.dict['args'] = spicemanip(botcom.dict['args'], '2+', 'list')

    return botcom


def trigger_hyphen_args(botcom):

    hyphen_args = []
    trigger_args_unhyphend = []
    for worditem in botcom.dict["args"]:
        if str(worditem).startswith("--"):
            clipped_word = str(worditem[2:]).lower()

            # valid arg above
            if clipped_word in prerun_shared.valid_hyphen_args:
                hyphen_args.append(clipped_word)

            # numbered args
            elif str(clipped_word).isdigit():
                hyphen_args.append(int(clipped_word))
            elif clipped_word in list(prerun_shared.numdict.keys()):
                hyphen_args.append(int(prerun_shared.numdict[clipped_word]))

            else:

                # check if arg word is a number
                try:
                    clipped_word = w2n.word_to_num(str(clipped_word))
                    hyphen_args.append(int(clipped_word))

                # word is not a valid arg or number
                except ValueError:
                    trigger_args_unhyphend.append(worditem)
        else:
            trigger_args_unhyphend.append(worditem)

    # only one arg allowed per && split
    if len(hyphen_args):
        hyphenarg = hyphen_args[0]
    else:
        hyphenarg = None

    return trigger_args_unhyphend, hyphenarg


def trigger_hyphen_arg_handler(bot, trigger, botcom):

    # Commands that cannot run via privmsg
    # TODO --check should work for commands that don't exist

    if not botcom.dict["hyphen_arg"]:
        return True

    # handle numbered args
    elif str(botcom.dict["hyphen_arg"]).isdigit() or botcom.dict["hyphen_arg"] in [-1, 'random']:
        return True

    elif botcom.dict["hyphen_arg"] in ['check']:
        if botcom.dict["com"].lower() != botcom.dict["realcom"]:
            botmessagelog.messagelog(botcom.dict["log_id"], botcom.dict["comtext"] + " is a valid alias command for " + botcom.dict["realcomtext"])
        else:
            botmessagelog.messagelog(botcom.dict["log_id"], botcom.dict["comtext"] + " is a valid command")
        return False

    elif botcom.dict["hyphen_arg"] in ['view']:
        if not len(botcom.dict["dict"][botcom.dict["responsekey"]]["responses"]):
            botmessagelog.messagelog(botcom.dict["log_id"], "The " + str(botcom.dict["realcom"]) + " " + str(botcom.dict["responsekey"] or '') + " command appears to have no entries!")
        else:
            botmessagelog.messagelog_private(botcom.dict["log_id"], "The " + str(botcom.dict["realcom"]) + " " + str(botcom.dict["responsekey"] or '') + " command contains:")
            listnumb, relist = 0, []
            for item in botcom.dict["dict"][botcom.dict["responsekey"]]["responses"]:
                listnumb += 1
                if isinstance(item, dict):
                    relist.append(str("[#" + str(listnumb) + "] COMPLEX dict Entry"))
                elif isinstance(item, list):
                    relist.append(str("[#" + str(listnumb) + "] COMPLEX list Entry"))
                else:
                    relist.append(str("[#" + str(listnumb) + "] " + str(item)))
            botmessagelog.messagelog_private(botcom.dict["log_id"], relist)
            return False

    elif botcom.dict["hyphen_arg"] in ['count']:
        botmessagelog.messagelog(botcom.dict["log_id"], "The " + str(botcom.dict["realcom"]) + " " + str(botcom.dict["responsekey"] or '') + " command has " + str(len(botcom.dict["dict"][botcom.dict["responsekey"]]["responses"])) + " entries.")
        return False

    elif botcom.dict["hyphen_arg"] in ['special', 'options', 'list']:
        if not len(botcom.dict["dict"]["nonstockoptions"]):
            botmessagelog.messagelog(botcom.dict["log_id"], "There appear to be no special options for " + str(botcom.dict["realcom"]) + ".")
        else:
            botmessagelog.messagelog(botcom.dict["log_id"], "The special options for " + str(botcom.dict["realcom"]) + " command include: " + spicemanip(botcom.dict["dict"]["nonstockoptions"], "andlist") + ".")
        return False

    elif botcom.dict["hyphen_arg"] in ['add', 'del', 'remove']:
        if botcom.dict["hyphen_arg"] in ['add', 'remove']:
            directionword = botcom.dict["hyphen_arg"]
        elif botcom.dict["hyphen_arg"] in ['del']:
            directionword = "remove"
        if not botcom.dict["dict"][botcom.dict["responsekey"]]["updates_enabled"]:
            botmessagelog.messagelog_error(botcom.dict["log_id"], "The " + str(botcom.dict["realcom"]) + " " + str(botcom.dict["responsekey"] or '') + " entry list cannot be updated.")

        fulltext = spicemanip(botcom.dict['args'], 0)
        if not fulltext:
            botmessagelog.messagelog(botcom.dict["log_id"], "What would you like to " + directionword + " from the " + str(botcom.dict["realcom"]) + " " + str(botcom.dict["responsekey"] or '') + " entry list?")
        return True

    elif botcom.dict["hyphen_arg"] in [
                                        'enable', 'disable',
                                        'block', 'unblock',
                                        "activate", "deactivate",
                                        "on", "off"
                                        ]:

        target = spicemanip(botcom.dict["args"], 1) or trigger.nick
        if not target:
            if botcom.dict["hyphen_arg"] in ['enable', 'unblock', "activate", "on"]:
                botmessagelog.messagelog_error(botcom.dict["log_id"], "Who/Where am I enabling " + str(botcom.dict["comtext"]) + " usage for?")
            else:
                botmessagelog.messagelog_error(botcom.dict["log_id"], "Who/Where am I disabling " + str(botcom.dict["comtext"]) + " usage for?")
            return False
        botcom.dict["args"] = spicemanip(botcom.dict["args"], "2+", "list")

        if not botdb.check_nick_id(target) and not botchannels.check_channel_bot(target, True):
            botmessagelog.messagelog_error(botcom.dict["log_id"], "I don't know who/what " + str(target) + " is.")
            return False

        if not botusers.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            if target != trigger.nick:
                if botcom.dict["hyphen_arg"] in ['enable', 'unblock', "activate", "on"]:
                    botmessagelog.messagelog_error(botcom.dict["log_id"], "I was unable to enable this command for " + str(target) + " due to privilege issues.")
                else:
                    botmessagelog.messagelog_error(botcom.dict["log_id"], "I was unable to disable this command for " + str(target) + " due to privilege issues.")
                return False

        if botcom.dict["hyphen_arg"] in ['enable', 'unblock', "activate", "on"]:

            if not botcommands.check_commands_disabled(botcom.dict["realcomref"], target):
                botmessagelog.messagelog_error(botcom.dict["log_id"], botcom.dict["comtext"] + " is already enabled for " + str(target))
                return False

            botcommands.unset_command_disabled(botcom.dict["realcomref"], target)
            botmessagelog.messagelog(botcom.dict["log_id"], botcom.dict["comtext"] + " is now enabled for " + str(target))
            return False

        else:

            if botcommands.check_commands_disabled(botcom.dict["realcomref"], target):
                botmessagelog.messagelog_error(botcom.dict["log_id"], botcom.dict["comtext"] + " is already disabled for " + str(target))
                return False

            trailingmessage = spicemanip(botcom.dict["args"], 0) or "No reason given."
            timestamp = str(datetime.datetime.utcnow())

            botcommands.set_command_disabled(botcom.dict["realcomref"], target, timestamp, trailingmessage, trigger.nick)
            botmessagelog.messagelog(botcom.dict["log_id"], botcom.dict["comtext"] + " is now disabled for " + str(target))
            return False

    if botcom.dict["hyphen_arg"] in ['multirun', 'multiruns']:

        onoff = spicemanip(botcom.dict["args"], 1) or None
        if not onoff or onoff not in ['enable', 'unblock', "activate", "on"]:
            botmessagelog.messagelog_error(botcom.dict["log_id"], "Do you want to enable or disable " + str(botcom.dict["comtext"]) + " multirun usage?")
            return False

        target = spicemanip(botcom.dict["args"], 1) or trigger.nick
        if not target:
            if onoff in ['enable', 'unblock', "activate", "on"]:
                botmessagelog.messagelog_error(botcom.dict["log_id"], "Who/Where am I enabling " + str(botcom.dict["comtext"]) + " multirun usage for?")
            else:
                botmessagelog.messagelog_error(botcom.dict["log_id"], "Who/Where am I disabling " + str(botcom.dict["comtext"]) + " multirun usage for?")
            return False
        botcom.dict["args"] = spicemanip(botcom.dict["args"], "2+", "list")

        if not botdb.check_nick_id(target) and not botchannels.check_channel_bot(target, True):
            botmessagelog.messagelog_error(botcom.dict["log_id"], "I don't know who/what " + str(target) + " is.")
            return False

        if not botusers.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
            if target != trigger.nick:
                if onoff in ['enable', 'unblock', "activate", "on"]:
                    botmessagelog.messagelog_error(botcom.dict["log_id"], "I was unable to enable multirun usage on " + str(botcom.dict["comtext"]) + " for " + str(target) + " due to privilege issues.")
                else:
                    botmessagelog.messagelog_error(botcom.dict["log_id"], "I was unable to enable multirun usage on " + str(botcom.dict["comtext"]) + " for " + str(target) + " due to privilege issues.")
                return False

        if onoff in ['enable', 'unblock', "activate", "on"]:

            if not botcommands.check_commands_disabled(botcom.dict["realcomref"], target, "multirun"):
                botmessagelog.messagelog_error(botcom.dict["log_id"], botcom.dict["comtext"] + " multirun is already enabled for " + str(target))
                return False

            botcommands.unset_command_disabled(botcom.dict["realcomref"], target, "multirun")
            botmessagelog.messagelog(botcom.dict["log_id"], botcom.dict["comtext"] + " multirun is now enabled for " + str(target))
            return False

        else:

            if botcommands.check_commands_disabled(botcom.dict["realcomref"], target, "multirun"):
                botmessagelog.messagelog_error(botcom.dict["log_id"], botcom.dict["comtext"] + " multirun is already disabled for " + str(target))
                return False

            trailingmessage = spicemanip(botcom.dict["args"], 0) or "No reason given."
            timestamp = str(datetime.datetime.utcnow())

            botcommands.set_command_disabled(botcom.dict["realcomref"], target, timestamp, trailingmessage, trigger.nick, "multirun")
            botmessagelog.messagelog(botcom.dict["log_id"], botcom.dict["comtext"] + " multirun is now disabled for " + str(target))
            return False

    elif botcom.dict["hyphen_arg"] in ['example', 'usage']:
        botmessagelog.messagelog(botcom.dict["log_id"], botcom.dict["comtext"] + ": " + str(botcom.dict["dict"]["example"]))
        return False

    elif botcom.dict["hyphen_arg"] in ['filename', 'filepath']:
        botmessagelog.messagelog(botcom.dict["log_id"], "The " + str(botcom.dict["comtext"]) + " file is located at " + str(botcom.dict["dict"][botcom.dict["hyphen_arg"]]))
        return False

    elif botcom.dict["hyphen_arg"] in ['foldername', 'folderpath']:
        botmessagelog.messagelog(botcom.dict["log_id"], "The " + str(botcom.dict["comtext"]) + " folder is located at " + str(botcom.dict["dict"][botcom.dict["hyphen_arg"]]))
        return False

    elif botcom.dict["hyphen_arg"] in ['author']:
        botmessagelog.messagelog(botcom.dict["log_id"], "The author of the " + str(botcom.dict["comtext"]) + " command is " + botcom.dict["dict"]["author"] + ".")
        return False

    elif botcom.dict["hyphen_arg"] in ['contribs', 'contrib', "contributors"]:
        botmessagelog.messagelog(botcom.dict["log_id"], "The contributors of the " + str(botcom.dict["comtext"]) + " command are " + spicemanip(botcom.dict["dict"]["contributors"], "andlist") + ".")
        return False

    elif botcom.dict["hyphen_arg"] in ['alias', 'aliases']:
        botmessagelog.messagelog(botcom.dict["log_id"], "The alaises of the " + str(botcom.dict["comtext"]) + " command are " + spicemanip(botcom.dict["dict"]["validcoms"], "andlist") + ".")
        return False

    return False
