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

import spicemanip

from .Logs import logs
from .Config import config as botconfig
from .Database import db as botdb


class SpiceBot_Commands_MainSection(StaticSection):
    query_prefix = ValidatedAttribute('query_prefix', default="?")


class BotCommands():
    """This Logs all commands known to the bot"""
    def __init__(self):
        self.setup_commands()
        self.lock = threading.Lock()
        self.dict = {
                    "counts": 0,
                    'nickrules': [],
                    'nickaiml': [],
                    "commands": {
                                'module': {},
                                'nickname': {},
                                'rule': {}
                                },
                    'disabled': {}
                    }
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
        for commandstype in list(self.dict['commands'].keys()):
            if commandstype not in ['rule']:
                for com in list(self.dict['commands'][commandstype].keys()):
                    if com.lower() == command.lower():
                        return commandstype
        return None

    def get_commands_disabled(self, channel):
        if not len(list(self.dict['disabled'])):
            self.dict['disabled'] = botdb.get_channel_value(channel, 'commands_disabled') or {}
        return self.dict['disabled']

    def check_commands_disabled(self, command, channel):
        if command in list(self.get_commands_disabled(channel).keys()):
            return True
        else:
            return False

    def get_realcom(self, command, trigger_command_type):
        realcom = command

        if trigger_command_type not in list(self.dict['commands'].keys()):
            return realcom

        if command not in list(self.dict['commands'][trigger_command_type].keys()):
            return realcom

        if "aliasfor" in self.dict['commands'][trigger_command_type][command].keys():
            realcom = self.dict['commands'][trigger_command_type][command]

        return realcom

    def set_command_disabled(self, command, channel, timestamp, reason, bywhom):
        if not len(list(self.dict['disabled'])):
            self.dict['disabled'] = botdb.get_channel_value(channel, 'commands_disabled') or {}
        self.dict['disabled'][command] = {"reason": reason, "timestamp": timestamp, "disabledby": bywhom}
        botdb.set_channel_value(channel, 'commands_disabled', self.dict['disabled'])

    def unset_command_disabled(self, command, channel):
        if not len(list(self.dict['disabled'])):
            self.dict['disabled'] = botdb.get_channel_value(channel, 'commands_disabled') or {}
        if command in list(self.dict['disabled'].keys()):
            del self.dict['disabled'][command]
        botdb.set_channel_value(channel, 'commands_disabled', self.dict['disabled'])

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
            comaliases = spicemanip.main(command_dict["validcoms"], '2+', 'list')
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
        try:
            import sopel_modules
            for plugin_dir in set(sopel_modules.__path__):
                for pathname in os.listdir(plugin_dir):
                    pypi_modules_dir = os.path.join(plugin_dir, pathname)
                    filepathlisting.append(pypi_modules_dir)
        except Exception as e:
            logs.log('SpiceBOT_COMMANDS', "sopel_modules not loaded :" + str(e))

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

            detected_lines = []
            for line in module_file_lines:

                if str(line).startswith("@"):
                    line = str(line)[1:]

                    if str(line).startswith(tuple(["commands", "module.commands", "sopel.module.commands"])):
                        line = str(line).split("commands")[-1]
                        line = "commands" + line
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

            if len(detected_lines):

                filelinelist = []
                currentsuccesslines = 0
                for detected_line in detected_lines:
                    try:

                        # Commands
                        if str(detected_line).startswith("commands"):
                            comtype = "module"
                            validcoms = eval(str(detected_line).split("commands")[-1])
                        elif str(detected_line).startswith("nickname_commands"):
                            comtype = "nickname"
                            validcoms = eval(str(detected_line).split("nickname_commands")[-1])
                        elif str(detected_line).startswith("rule"):
                            comtype = "rule"
                            validcoms = eval(str(detected_line).split("rule")[-1])

                        if isinstance(validcoms, tuple):
                            validcoms = list(validcoms)
                        else:
                            validcoms = [validcoms]
                        for regexcom in ["(.*)", '^\?(.*)']:
                            if regexcom in validcoms:
                                while regexcom in validcoms:
                                    validcoms.remove(regexcom)

                        if len(validcoms):
                            validcomdict = {
                                            "comtype": comtype,
                                            "validcoms": validcoms,
                                            "filepath": str(modulefile),
                                            "filename": str(filename_base),
                                            "folderpath": str(folderpath),
                                            "foldername": str(foldername),
                                            }
                            filelinelist.append(validcomdict)
                            currentsuccesslines += 1
                    except Exception as e:
                        addnothing = e
                        if addnothing:
                            currentsuccesslines += 0

                if len(filelinelist):
                    for vcomdict in filelinelist:
                        self.register(vcomdict)


commands = BotCommands()
