# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Commands system.

This Class stores commands in an easy to access manner
"""

import sopel
from sopel.config.types import StaticSection, ValidatedAttribute

import os
import threading
import copy
import imp

from sopel_modules.spicemanip import spicemanip
import sopel_modules

from .Logs import logs
from .Config import config as botconfig
from .Database import db as botdb
from .Read import read as botread
from .Channels import channels as botchannels
from .Users import users as botusers


class SpiceBot_Commands_MainSection(StaticSection):
    query_prefix = ValidatedAttribute('query_prefix', default="?")


class BotCommands():
    """This Logs all commands known to the bot"""
    def __init__(self):
        self.setup_commands()
        self.lock = threading.Lock()
        self.dict = {
                    'nickrules': [],
                    'nickaiml': [],
                    "commands": {
                                'module': {},
                                'nickname': {},
                                'rule': {}
                                },
                    'disabled': {},
                    }
        self.todo_list = []
        self.module_files_parse()
        self.nickrules()
        for comtype in ['module', 'nickname', 'rule']:
            logs.log('SpiceBot_Commands', "Found " + str(len(list(self.dict['commands'][comtype].keys()))) + " " + comtype + " commands.", True)

    def setup_commands(self):
        botconfig.define_section("SpiceBot_Commands", SpiceBot_Commands_MainSection, validate=False)
        botconfig.core.query_list = str(botconfig.SpiceBot_Commands.query_prefix).replace("\\", '').split("|")
        botconfig.core.prefix_list.extend(botconfig.SpiceBot_Commands.query_prefix)

    def nickrules(self):
        for command in list(self.dict['commands']['rule'].keys()):
            if command.startswith("$nickname"):
                command = command.split("$nickname")[-1]
                if command not in self.dict['nickrules']:
                    self.dict['nickrules'].append(command)

    def find_command_type(self, command):
        commandtype_list = list(self.dict['commands'].keys())
        if 'rule' in commandtype_list:
            commandtype_list.remove('rule')
        for commandstype in commandtype_list:
            for com in list(self.dict['commands'][commandstype].keys()):
                if com.lower() == command.lower():
                    return commandstype
        return None

    def get_command_dict(self, command, trigger_command_type=None):
        if not trigger_command_type:
            trigger_command_type = self.find_command_type(command)
            if not trigger_command_type:
                return {}
        command_dict = copy.deepcopy(self.dict['commands'][trigger_command_type][command])
        return command_dict

    def get_realcom(self, command, trigger_command_type):
        realcom = command

        if trigger_command_type not in list(self.dict['commands'].keys()):
            return realcom

        if command not in list(self.dict['commands'][trigger_command_type].keys()):
            return realcom

        if "aliasfor" in self.dict['commands'][trigger_command_type][command].keys():
            realcom = self.dict['commands'][trigger_command_type][command]["aliasfor"]

        return realcom

    def chan_or_nick(self, target):
        if botchannels.check_channel_bot(target, True):
            return "channel"
        elif botdb.check_nick_id(target):
            return "nick"
        else:
            raise Exception(str(target.lower()) + " appears to not be a valid user/channel")

    def get_commands_disabled(self, target, disabletype="fully"):
        disabletype = str(disabletype)
        target_type = self.chan_or_nick(target)
        if disabletype not in list(self.dict['disabled'].keys()):
            self.dict['disabled'][disabletype] = {
                                                    "nick": {},
                                                    "channel": {}
                                                    }
        if target_type == "nick":
            nick_id = botusers.ID(target)
            if nick_id not in list(self.dict['disabled'][disabletype]["nick"].keys()):
                self.dict['disabled'][disabletype]["nick"][nick_id] = botdb.get_nick_value(target, 'commands_' + disabletype + 'disabled') or {}
            return self.dict['disabled'][disabletype]["nick"][nick_id]
        elif target_type == "channel":
            target = str(target).lower()
            if target not in list(self.dict['disabled'][disabletype]["channel"].keys()):
                self.dict['disabled'][disabletype]["channel"][target] = botdb.get_channel_value(target, 'commands_' + disabletype + 'disabled') or {}
            return self.dict['disabled'][disabletype]["channel"][target]
        else:
            raise Exception(str(target.lower()) + " appears to not be a valid user/channel")

    def check_commands_disabled(self, command, target, disabletype="fully"):
        command = str(command).lower()
        if command in list(self.get_commands_disabled(target, disabletype).keys()):
            return True
        else:
            return False

    def set_command_disabled(self, command, target, timestamp, reason, bywhom, disabletype="fully"):
        command = str(command).lower()
        disabletype = str(disabletype)
        target_type = self.chan_or_nick(target)
        if disabletype not in list(self.dict['disabled'].keys()):
            self.dict['disabled'][disabletype] = {
                                                    "nick": {},
                                                    "channel": {}
                                                    }
        if target_type == "nick":
            nick_id = botusers.ID(target)
            if nick_id not in list(self.dict['disabled'][disabletype]["nick"].keys()):
                self.dict['disabled'][disabletype]["nick"][nick_id] = botdb.get_nick_value(target, 'commands_' + disabletype + 'disabled') or {}
            self.dict['disabled'][disabletype]["nick"][nick_id][command] = {"reason": reason, "timestamp": timestamp, "disabledby": bywhom}
            botdb.set_nick_value(target, 'commands_' + disabletype + 'disabled', self.dict['disabled'][disabletype]["nick"][nick_id])
        elif target_type == "channel":
            target = str(target).lower()
            if target not in list(self.dict['disabled'][disabletype]["channel"].keys()):
                self.dict['disabled'][disabletype]["channel"][target] = botdb.get_channel_value(target, 'commands_' + disabletype + 'disabled') or {}
            self.dict['disabled'][disabletype]["channel"][target][command] = {"reason": reason, "timestamp": timestamp, "disabledby": bywhom}
            botdb.set_channel_value(target, 'commands_' + disabletype + 'disabled', self.dict['disabled'][disabletype]["channel"][target])
        else:
            raise Exception(str(target.lower()) + " appears to not be a valid user/channel")

    def unset_command_disabled(self, command, target, disabletype="fully"):
        command = str(command).lower()
        disabletype = str(disabletype)
        target_type = self.chan_or_nick(target)
        if disabletype not in list(self.dict['disabled'].keys()):
            self.dict['disabled'][disabletype] = {
                                                    "nick": {},
                                                    "channel": {}
                                                    }
        if target_type == "nick":
            nick_id = botusers.ID(target)
            if nick_id not in list(self.dict['disabled'][disabletype]["nick"].keys()):
                self.dict['disabled'][disabletype]["nick"][nick_id] = botdb.get_nick_value(target, 'commands_' + disabletype + 'disabled') or {}
            if command in list(self.dict['disabled'][disabletype]["nick"][nick_id].keys()):
                del self.dict['disabled'][disabletype]["nick"][nick_id][command]
            botdb.set_nick_value(target, 'commands_' + disabletype + 'disabled', self.dict['disabled'][disabletype]["nick"][nick_id])
        elif target_type == "channel":
            target = str(target).lower()
            if target not in list(self.dict['disabled'][disabletype]["channel"].keys()):
                self.dict['disabled'][disabletype]["nick"][target] = botdb.get_channel_value(target, 'commands_' + disabletype + 'disabled') or {}
            if command in list(self.dict['disabled'][disabletype]["channel"][target].keys()):
                del self.dict['disabled'][disabletype]["channel"][target][command]
            botdb.set_channel_value(target, 'commands_' + disabletype + 'disabled', self.dict['disabled'][disabletype]["channel"][target])
        else:
            raise Exception(str(target.lower()) + " appears to not be a valid user/channel")

    def register(self, command_dict):

        self.lock.acquire()

        command_type = command_dict["comtype"]
        if command_type not in list(self.dict['commands'].keys()):
            self.dict['commands'][command_type] = dict()

        # default command to filename
        if "validcoms" not in list(command_dict.keys()):
            command_dict["validcoms"] = [command_dict["filename"]]

        validcoms = command_dict["validcoms"]
        if not isinstance(validcoms, list):
            validcoms = [validcoms]

        maincom = command_dict["validcoms"][0]
        if len(command_dict["validcoms"]) > 1:
            comaliases = spicemanip(command_dict["validcoms"], '2+', 'list')
        else:
            comaliases = []

        self.dict['commands'][command_type][maincom] = command_dict
        for comalias in comaliases:
            if comalias not in list(self.dict['commands'][command_type].keys()):
                self.dict['commands'][command_type][comalias] = {"aliasfor": maincom}

        self.lock.release()

    def module_directory_list(self):
        filepathlisting = []

        # main Modules directory
        main_dir = os.path.dirname(os.path.abspath(sopel.__file__))
        modules_dir = os.path.join(main_dir, 'modules')
        filepathlisting.append(modules_dir)

        # Home Directory
        home_modules_dir = os.path.join(botconfig.homedir, 'modules')
        if os.path.isdir(home_modules_dir):
            filepathlisting.append(home_modules_dir)

        # pypi installed
        for plugin_dir in set(sopel_modules.__path__):
            for pathname in os.listdir(plugin_dir):
                pypi_modules_dir = os.path.join(plugin_dir, pathname)
                filepathlisting.append(pypi_modules_dir)

        # Extra directories
        for directory in botconfig.extra:
            filepathlisting.append(directory)

        return filepathlisting

    def module_files_list(self):
        filepathlisting = self.module_directory_list()

        filepathlist = []

        for directory in filepathlisting:
            for pathname in os.listdir(directory):
                path = os.path.join(directory, pathname)
                if (os.path.isfile(path) and path.endswith('.py') and not path.startswith('_')):
                    if pathname not in ["SpiceBot_dummycommand.py"]:
                        filepathlist.append(str(path))

        # CoreTasks
        main_dir = os.path.dirname(os.path.abspath(sopel.__file__))
        ct_path = os.path.join(main_dir, 'coretasks.py')
        filepathlist.append(ct_path)

        return filepathlist

    def module_files_parse(self):
        filepathlist = self.module_files_list()

        for modulefile in filepathlist:

            module_file_lines = []
            module_file = open(modulefile, 'r')
            lines = module_file.readlines()
            for line in lines:
                module_file_lines.append(line)
            module_file.close()

            # gather file stats
            slashsplit = str(modulefile).split("/")
            filename = slashsplit[-1]
            filename_base = os.path.basename(filename).rsplit('.', 1)[0]
            folderpath = str(modulefile).split("/" + filename)[0]
            foldername = str(folderpath).split("/")[-1]

            # check for json reference file
            comdict = botread.module_json_to_dict(str(modulefile))

            # replace json defaults
            comdict["filepath"] = str(modulefile)
            comdict["filename"] = str(filename_base)
            comdict["folderpath"] = str(folderpath)
            comdict["foldername"] = str(foldername)

            detected_lines = []
            todo_list = []
            for line in module_file_lines:

                if str(line).startswith("@"):
                    line = str(line)[1:]

                    if str(line).startswith(tuple(["commands", "module.commands", "sopel.module.commands"])):
                        line = str(line).split("commands")[-1]
                        line = "commands" + line
                        detected_lines.append(line)
                    elif str(line).startswith(tuple(["action_commands", "module.action_commands", "sopel.module.action_commands"])):
                        line = str(line).split("action_commands")[-1]
                        line = "action_commands" + line
                        detected_lines.append(line)
                    elif str(line).startswith(tuple(["nickname_commands", "module.nickname_commands", "sopel.module.nickname_commands"])):
                        line = str(line).split("nickname_commands")[-1]
                        line = "nickname_commands" + line
                        detected_lines.append(line)
                    elif str(line).startswith(tuple(["rule", "module.rule", "sopel.module.rule"])):
                        line = str(line).split("rule")[-1]
                        line = "rule" + line
                    else:
                        line = None

                    if line:
                        detected_lines.append(line)

                elif "TODO" in str(line):
                    todo_list.append(str(line))

            if len(todo_list):
                self.todo_list.extend(todo_list)

            if len(detected_lines):

                filelinelist = []
                for detected_line in detected_lines:
                    validcomdict = copy.deepcopy(comdict)

                    validcomdict["TODO"] = todo_list

                    # Commands
                    if str(detected_line).startswith("commands"):
                        comtype = "module"
                        try:
                            validcoms = eval(str(detected_line).split("commands")[-1])
                        except Exception as e:
                            validcoms = e
                            validcoms = []
                    elif str(detected_line).startswith("action_commands"):
                        comtype = "action"
                        try:
                            validcoms = eval(str(detected_line).split("action_commands")[-1])
                        except Exception as e:
                            validcoms = e
                            validcoms = []
                    elif str(detected_line).startswith("nickname_commands"):
                        comtype = "nickname"
                        try:
                            validcoms = eval(str(detected_line).split("nickname_commands")[-1])
                        except Exception as e:
                            validcoms = e
                            validcoms = []
                    elif str(detected_line).startswith("rule"):
                        comtype = "rule"
                        try:
                            validcoms = eval(str(detected_line).split("rule")[-1])
                        except Exception as e:
                            validcoms = e
                            validcoms = []

                    if isinstance(validcoms, tuple):
                        validcoms = list(validcoms)
                    if not isinstance(validcoms, list):
                        validcoms = [validcoms]
                    for regexcom in ["(.*)", '^\?(.*)']:
                        if regexcom in validcoms:
                            while regexcom in validcoms:
                                validcoms.remove(regexcom)

                    if len(validcoms):
                        validcomdict["comtype"] = comtype
                        validcomdict["validcoms"] = validcoms
                        filelinelist.append(validcomdict)

                        self.register(validcomdict)

    def list_plugin_filenames(self, directory):
        return_list = []
        base = os.path.abspath(directory)
        for filename in os.listdir(base):
            abspath = os.path.join(base, filename)

            if os.path.isdir(abspath):
                returndict = {"type": "folder"}
                if os.path.isfile(os.path.join(abspath, '__init__.py')):
                    returndict["name"] = filename
                    returndict["abspath"] = abspath
                    module_files = []
                    for subfilename in os.listdir(abspath):
                        name, ext = os.path.splitext(subfilename)
                        if ext == '.py' and name != '__init__':
                            subabspath = os.path.join(abspath, subfilename)
                            if os.path.isfile(os.path.join(subabspath, name + '.json')):
                                dictfile = os.path.join(subabspath, name + '.json')
                            else:
                                dictfile = False
                            module_files.append({"name": name, "abspath": subabspath, "dictfile": dictfile})
                    returndict["module_files"] = module_files
                    return_list.append(returndict)
        else:
            returndict = {"type": "file"}
            name, ext = os.path.splitext(filename)
            if ext == '.py' and name != '__init__':
                returndict["name"] = name
                returndict["abspath"] = abspath
                if os.path.isfile(os.path.join(abspath, name + '.json')):
                    dictfile = os.path.join(abspath, name + '.json')
                else:
                    dictfile = False
                returndict["dictfile"] = dictfile
                return_list.append(returndict)
        return return_list

    def list_plugin_dir(self):
        plugin_dir = imp.find_module('modules', [imp.find_module('sopel')[1]])[1]
        return self.list_plugin_filenames(plugin_dir)

    def list_sopel_modules_dir(self):
        try:
            import sopel_modules
        except ImportError:
            return []
        sopel_modules_list = []
        for plugin_dir in set(sopel_modules.__path__):
            small_list = self.list_plugin_filenames(plugin_dir)
            sopel_modules_list.extend(small_list)
        return sopel_modules_list

    def get_plugin_list(self):
        full_list = []
        for x in ["plugin", "sopel_modules"]:
            return_list = eval("self.list_" + str(x) + "_dir()")
            full_list.extend(return_list)
        return full_list



commands = BotCommands()
