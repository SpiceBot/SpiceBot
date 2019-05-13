# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel
import sopel.module

import os

from sopel_modules.SpiceBot_Events.System import bot_events_startup_register, bot_events_recieved, bot_events_trigger
from sopel_modules.SpiceBot_SBTools import bot_logging

import spicemanip


def setup(bot):
    bot_logging(bot, 'SpiceBot_CommandsQuery', "Starting setup procedure")
    bot_events_startup_register(bot, ['2002'])

    if 'SpiceBot_CommandsQuery' not in bot.memory:
        bot.memory['SpiceBot_CommandsQuery'] = {"counts": 0, "commands": {}, "nickrules": []}

    for comtype in ['module', 'nickname', 'rule']:
        if comtype not in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
            bot.memory['SpiceBot_CommandsQuery']['commands'][comtype] = dict()

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
        bot_logging(bot, 'SpiceBot_CommandsQuery', "sopel_modules not loaded :" + str(e))

    # Extra directories
    filepathlist = []
    for directory in bot.config.core.extra:
        filepathlisting.append(directory)

    for directory in filepathlisting:
        for pathname in os.listdir(directory):
            path = os.path.join(directory, pathname)
            if (os.path.isfile(path) and path.endswith('.py') and not path.startswith('_')):
                if pathname not in ["SpiceBot_dummycommand.py"]:
                    filepathlist.append(str(path))

    # CoreTasks
    ct_path = os.path.join(main_dir, 'coretasks.py')
    filepathlist.append(ct_path)

    for modulefile in filepathlist:

        module_file_lines = []
        module_file = open(modulefile, 'r')
        lines = module_file.readlines()
        for line in lines:
            module_file_lines.append(line)
        module_file.close()

        dict_from_file = dict()

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
                if "(.*)" in validcoms:
                    while "(.*)" in validcoms:
                        validcoms.remove("(.*)")

                if len(validcoms):
                    validcomdict = {"comtype": comtype, "validcoms": validcoms}
                    filelinelist.append(validcomdict)
                    currentsuccesslines += 1

            if currentsuccesslines:
                bot.memory['SpiceBot_CommandsQuery']['counts'] += 1

            if len(filelinelist):
                for atlinefound in filelinelist:

                    dict_from_file = dict()

                    comtype = atlinefound["comtype"]
                    validcoms = atlinefound["validcoms"]

                    # default command to filename
                    if "validcoms" not in dict_from_file.keys():
                        dict_from_file["validcoms"] = validcoms

                    maincom = dict_from_file["validcoms"][0]
                    if len(dict_from_file["validcoms"]) > 1:
                        comaliases = spicemanip.main(dict_from_file["validcoms"], '2+', 'list')
                    else:
                        comaliases = []

                    bot.memory['SpiceBot_CommandsQuery']['commands'][comtype][maincom] = dict_from_file
                    for comalias in comaliases:
                        if comalias not in bot.memory['SpiceBot_CommandsQuery']['commands'][comtype].keys():
                            bot.memory['SpiceBot_CommandsQuery']['commands'][comtype][comalias] = {"aliasfor": maincom}

    for comtype in ['module', 'nickname', 'rule']:
        bot_logging(bot, 'SpiceBot_CommandsQuery', "Found " + str(len(bot.memory['SpiceBot_CommandsQuery']['commands'][comtype].keys())) + " " + comtype + " commands.", True)

    for command in bot.memory['SpiceBot_CommandsQuery']['commands']['rule'].keys():
        if command.startswith("$nickname"):
            command = command.split("$nickname")[-1]
            if command not in bot.memory['SpiceBot_CommandsQuery']['nickrules']:
                bot.memory['SpiceBot_CommandsQuery']['nickrules'].append(command)

    bot_events_trigger(bot, 2002, "SpiceBot_CommandsQuery")


def shutdown(bot):
    if "SpiceBot_CommandsQuery" in bot.memory:
        del bot.memory["SpiceBot_CommandsQuery"]


@sopel.module.event('1004')
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    for comtype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        if comtype not in ['module', 'nickname', 'rule']:
            bot_logging(bot, 'SpiceBot_CommandsQuery', "Found " + str(len(bot.memory['SpiceBot_CommandsQuery']['commands'][comtype].keys())) + " " + comtype + " commands.", True)


def commandsquery_register(bot, command_type, validcoms, aliasfor=None):

    if 'SpiceBot_CommandsQuery' not in bot.memory:
        bot.memory['SpiceBot_CommandsQuery'] = {"counts": 0, "commands": {}, "nickrules": []}

    if not isinstance(validcoms, list):
        validcoms = [validcoms]

    if command_type not in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        bot.memory['SpiceBot_CommandsQuery']['commands'][command_type] = dict()
    bot.memory['SpiceBot_CommandsQuery']['counts'] += 1

    dict_from_file = dict()

    # default command to filename
    if "validcoms" not in dict_from_file.keys():
        dict_from_file["validcoms"] = validcoms

    if not aliasfor:

        maincom = dict_from_file["validcoms"][0]
        if len(dict_from_file["validcoms"]) > 1:
            comaliases = spicemanip.main(dict_from_file["validcoms"], '2+', 'list')
        else:
            comaliases = []
        bot.memory['SpiceBot_CommandsQuery']['commands'][command_type][maincom] = dict_from_file
    else:
        comaliases = validcoms

    for comalias in comaliases:
        if comalias not in bot.memory['SpiceBot_CommandsQuery']['commands'][command_type].keys():
            bot.memory['SpiceBot_CommandsQuery']['commands'][command_type][comalias] = {"aliasfor": aliasfor}


@sopel.module.event('2002')
@sopel.module.rule('.*')
def bot_events_setup(bot, trigger):
    bot_events_recieved(bot, trigger.event)
