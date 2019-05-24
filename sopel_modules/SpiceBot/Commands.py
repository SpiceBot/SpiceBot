# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Commands system.

This Class stores commands in an easy to access manner
"""
import sopel
import os
import threading

import spicemanip

from .Logs import logs
from .Database import db as spicedb


class BotCommands():
    """This Logs all commands known to the bot"""
    def __init__(self):
        self.lock = threading.Lock()
        self.dict = {
                    "counts": 0,
                    "commands": {
                                'module': {},
                                'nickname': {},
                                'rule': {}
                                },
                    'disabled': {}
                    }

    def find_command_type(self, command):
        for commandstype in self.dict['commands'].keys():
            if commandstype not in ['rule']:
                for com in self.dict['commands'][commandstype].keys():
                    if com.lower() == command.lower():
                        return commandstype
        return None

    def get_disabled_commands(self, bot, channel):
        if not len(list(self.dict['disabled'])):
            self.dict['disabled'] = spicedb.get_channel_value(bot, channel, 'disabled_commands', 'commands') or {}
        return self.dict['disabled']

    def check_disabled_commands(self, bot, command, channel):
        if command in self.get_disabled_commands(bot, channel).keys():
            return True
        else:
            return False

    def get_realcom(self, command, trigger_command_type):
        commands_list = dict()
        for commandstype in self.dict['commands'][trigger_command_type].keys():
            for com in self.dict['commands'][commandstype].keys():
                if com not in commands_list.keys():
                    commands_list[com] = self.dict['commands'][commandstype][com]
        realcom = command
        if "aliasfor" in commands_list[command['com']].keys():
            realcom = commands_list[command['com']]["aliasfor"]
        return realcom

    def set_command_disabled(self, bot, command, channel, timestamp, reason, bywhom):
        if not len(list(self.dict['disabled'])):
            self.dict['disabled'] = spicedb.get_channel_value(bot, channel, 'disabled_commands', 'commands') or {}
        self.dict['disabled'][command] = {"reason": reason, "timestamp": timestamp, "disabledby": bywhom}
        spicedb.set_channel_value(bot, channel, 'disabled_commands', self.dict['disabled'], 'commands')

    def unset_command_disabled(self, bot, command, channel):
        if not len(list(self.dict['disabled'])):
            self.dict['disabled'] = spicedb.get_channel_value(bot, channel, 'disabled_commands', 'commands') or {}
        if command in self.dict['disabled'].keys():
            del self.dict['disabled'][command]
        spicedb.set_channel_value(bot, channel, 'disabled_commands', self.dict['disabled'], 'commands')

    def register(self, bot, command_dict):

        self.lock.acquire()

        command_type = command_dict["comtype"]
        validcoms = command_dict["validcoms"]

        if not isinstance(validcoms, list):
            validcoms = [validcoms]

        if command_type not in self.dict['commands'].keys():
            self.dict['commands'][command_type] = dict()

        dict_from_file = dict()

        # default command to filename
        if "validcoms" not in dict_from_file.keys():
            dict_from_file["validcoms"] = validcoms

        maincom = dict_from_file["validcoms"][0]
        if len(dict_from_file["validcoms"]) > 1:
            comaliases = spicemanip.main(dict_from_file["validcoms"], '2+', 'list')
        else:
            comaliases = []

        self.dict['commands'][command_type][maincom] = dict_from_file
        for comalias in comaliases:
            if comalias not in self.dict['commands'][command_type].keys():
                self.dict['commands'][command_type][comalias] = {"aliasfor": maincom}

        self.lock.release()

    def module_directory_list(self, bot):
        filepathlisting = []

        # main Modules directory
        main_dir = os.path.dirname(os.path.abspath(sopel.__file__))
        modules_dir = os.path.join(main_dir, 'modules')
        filepathlisting.append(modules_dir)

        # Home Directory
        home_modules_dir = os.path.join(bot.config.homedir, 'modules')
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
            logs.log('SpiceBot_CommandsQuery', "sopel_modules not loaded :" + str(e))

        # Extra directories
        for directory in bot.config.core.extra:
            filepathlisting.append(directory)

        return filepathlisting

    def module_files_list(self, bot):
        filepathlisting = self.module_directory_list(bot)

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

    def module_files_parse(self, bot):
        filepathlist = self.module_files_list(bot)

        for modulefile in filepathlist:

            module_file_lines = []
            module_file = open(modulefile, 'r')
            lines = module_file.readlines()
            for line in lines:
                module_file_lines.append(line)
            module_file.close()

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
                        validcomdict = {"comtype": comtype, "validcoms": validcoms}
                        filelinelist.append(validcomdict)
                        currentsuccesslines += 1

                if currentsuccesslines:
                    self.dict['counts'] += 1

                if len(filelinelist):
                    for atlinefound in filelinelist:
                        self.register(bot, atlinefound)


commands = BotCommands()
