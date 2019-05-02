# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel
from sopel import module
from sopel.tools import stderr

import os
from difflib import SequenceMatcher
from operator import itemgetter
import threading


from sopel_modules.SpiceBot_SBTools.BotEvents import set_bot_event


import spicemanip


def configure(config):
    pass


def setup(bot):
    stderr("[Sopel-CommandsQuery] Evaluating Core Commands List")

    threading.Thread(target=setup_thread, args=(bot,)).start()


def setup_thread(bot):

    bot.memory['Sopel-CommandsQuery'] = dict()
    for comtype in ['module', 'nickname', 'rule']:
        bot.memory['Sopel-CommandsQuery'][comtype + "_commands"] = dict()
        bot.memory['Sopel-CommandsQuery'][comtype + "_commands_count"] = 0

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
        pypi_modules = os.path.dirname(os.path.abspath(sopel_modules.__file__))
        pypi_modules_dir = os.path.join(pypi_modules, 'modules')
        filepathlisting.append(pypi_modules_dir)
    except Exception:
        pass

    # Extra directories
    filepathlist = []
    for directory in bot.config.core.extra:
        filepathlisting.append(directory)

    for directory in filepathlisting:
        for pathname in os.listdir(directory):
            path = os.path.join(directory, pathname)
            if (os.path.isfile(path) and path.endswith('.py') and not path.startswith('_')):
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
        filelinelist = []

        for line in module_file_lines:

            if str(line).startswith("@"):
                line = str(line)[1:]

                # Commands
                if str(line).startswith(tuple(["commands", "module.commands", "sopel.module.commands"])):
                    comtype = "module"
                    line = str(line).split("commands(")[-1]
                    line = str("(" + line)
                    validcoms = eval(str(line))
                    if isinstance(validcoms, tuple):
                        validcoms = list(validcoms)
                    else:
                        validcoms = [validcoms]
                    validcomdict = {"comtype": comtype, "validcoms": validcoms}
                    filelinelist.append(validcomdict)
                elif str(line).startswith(tuple(["nickname_commands", "module.nickname_commands", "sopel.module.nickname_commands"])):
                    comtype = "nickname"
                    line = str(line).split("commands(")[-1]
                    line = str("(" + line)
                    validcoms = eval(str(line))
                    if isinstance(validcoms, tuple):
                        validcoms = list(validcoms)
                    else:
                        validcoms = [validcoms]
                    nickified = []
                    for nickcom in validcoms:
                        nickified.append(str(bot.nick) + " " + nickcom)
                    validcomdict = {"comtype": comtype, "validcoms": nickified}
                    filelinelist.append(validcomdict)
                elif str(line).startswith(tuple(["rule", "module.rule", "sopel.module.rule"])):
                    comtype = "rule"
                    line = str(line).split("rule(")[-1]
                    validcoms = [str("(" + line)]
                    validcomdict = {"comtype": comtype, "validcoms": validcoms}
                    filelinelist.append(validcomdict)

        for atlinefound in filelinelist:

            comtype = atlinefound["comtype"]
            validcoms = atlinefound["validcoms"]

            comtypedict = str(comtype + "_commands")

            bot.memory['Sopel-CommandsQuery'][comtypedict + "_count"] += 1

            # default command to filename
            if "validcoms" not in dict_from_file.keys():
                dict_from_file["validcoms"] = validcoms

            maincom = dict_from_file["validcoms"][0]
            if len(dict_from_file["validcoms"]) > 1:
                comaliases = spicemanip.main(dict_from_file["validcoms"], '2+', 'list')
            else:
                comaliases = []

            bot.memory['Sopel-CommandsQuery'][comtypedict][maincom] = dict_from_file
            for comalias in comaliases:
                if comalias not in bot.memory['Sopel-CommandsQuery'][comtypedict].keys():
                    bot.memory['Sopel-CommandsQuery'][comtypedict][comalias] = {"aliasfor": maincom}

    for comtype in ['module_commands', 'nickname_commands', 'rule_commands']:
        stderr("[Sopel-CommandsQuery] Found " + str(len(bot.memory['Sopel-CommandsQuery'][comtype].keys())) + " " + comtype + " commands.")

    set_bot_event(bot, "Sopel-CommandsQuery")


@module.rule('^\?(.*)')
def query_detection(bot, trigger):

    while "Sopel-CommandsQuery" not in bot.memory:
        pass

    # command must start with
    if not str(trigger).startswith(tuple(['?'])):
        return
    stderr(trigger.args)

    commands_list = dict()
    for commandstype in bot.memory['Sopel-CommandsQuery'].keys():
        if not commandstype.endswith("_count"):
            for com in bot.memory['Sopel-CommandsQuery'][commandstype].keys():
                if com not in commands_list.keys():
                    commands_list[com] = bot.memory['Sopel-CommandsQuery'][commandstype][com]

    triggerargsarray = spicemanip.main(trigger, 'create')

    # command issued, check if valid
    querycommand = spicemanip.main(triggerargsarray, 1).lower()[1:]
    if len(querycommand) == 1:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(querycommand):
                commandlist.append(command)
        if commandlist == []:
            bot.notice("No commands match " + str(querycommand) + ".", trigger.nick)
            return
        else:
            bot.notice("The following commands match " + str(querycommand) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
            return

    elif querycommand.endswith(tuple(["+"])):
        querycommand = querycommand[:-1]
        if querycommand not in commands_list.keys():
            bot.notice("The " + str(querycommand) + " does not appear to be valid.")
            return
        realcom = querycommand
        if "aliasfor" in commands_list[querycommand].keys():
            realcom = commands_list[querycommand]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.notice("The following commands match " + str(querycommand) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick)
        return

    elif querycommand.endswith(tuple(['?'])):
        querycommand = querycommand[:-1]
        sim_com, sim_num = [], []
        for com in commands_list.keys():
            similarlevel = SequenceMatcher(None, querycommand.lower(), com.lower()).ratio()
            sim_com.append(com)
            sim_num.append(similarlevel)
        sim_num, sim_com = (list(x) for x in zip(*sorted(zip(sim_num, sim_com), key=itemgetter(0))))
        closestmatch = spicemanip.main(sim_com, 'reverse', "list")
        listnumb, relist = 1, []
        for item in closestmatch:
            if listnumb <= 10:
                relist.append(str(item))
            listnumb += 1
        bot.notice("The following commands may match " + str(querycommand) + ": " + spicemanip.main(relist, 'andlist') + ".", trigger.nick)
        return

    elif querycommand in commands_list.keys():
        bot.notice("The following commands match " + str(querycommand) + ": " + str(querycommand) + ".", trigger.nick)
        return

    elif not querycommand:
        return

    else:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(querycommand):
                commandlist.append(command)
        if commandlist == []:
            bot.notice("No commands match " + str(querycommand) + ".", trigger.nick)
            return
        else:
            bot.notice("The following commands match " + str(querycommand) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
            return


def commandsquery_register(bot, command_type, validcoms, aliasfor=None):

    if not isinstance(validcoms, list):
        validcoms = [validcoms]

    if 'Sopel-CommandsQuery' not in bot.memory:
        bot.memory['Sopel-CommandsQuery'] = dict()

    if command_type not in bot.memory['Sopel-CommandsQuery'].keys():
        bot.memory['Sopel-CommandsQuery'][command_type] = dict()
        bot.memory['Sopel-CommandsQuery'][command_type + "_count"] = 0
    bot.memory['Sopel-CommandsQuery'][command_type + "_count"] += 1

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
        bot.memory['Sopel-CommandsQuery'][command_type][maincom] = dict_from_file
    else:
        comaliases = validcoms

    for comalias in comaliases:
        if comalias not in bot.memory['Sopel-CommandsQuery'][command_type].keys():
            bot.memory['Sopel-CommandsQuery'][command_type][comalias] = {"aliasfor": aliasfor}
