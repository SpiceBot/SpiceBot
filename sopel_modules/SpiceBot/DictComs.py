# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot JSON Commands system.

This Class stores commands in an easy to access manner
"""

from sopel.config.types import StaticSection, ListAttribute

from .Config import config as botconfig
from .Read import read as botread
from .Commands import commands as botcommands
from .Database import db as botdb
from .Tools import prerun_shared

import os
import copy


class SpiceBot_DictComs_MainSection(StaticSection):
    extra = ListAttribute('extra')


class BotDictCommands():

    def __init__(self):
        self.setup_dictcoms()
        self.valid_com_types = [
                                'simple', 'fillintheblank', 'target', 'targetplusreason',
                                'sayings', "readfromfile", "readfromurl",
                                "ascii_art", "gif", "translate", "responses",
                                "feeds", "search"
                                ]
        self.dict_required = ["?default"]
        self.builtin_keys = [
                            "filepath", "filename", "folderpath", "foldername",
                            "comtype", "type", "validcoms",
                            "author", "contributors",
                            "description", "exampleresponse", "example",
                            "privs"
                            ]

        self.dictcom_load()

    def get_dict(self, triggersb):

        # simplify usage of the bot command going forward
        # copy dict to not overwrite
        triggersb['comdict'] = copy.deepcopy(botcommands.dict['commands']["dictcom"][triggersb['realcom']])

        # execute function based on command type
        triggersb['comtype'] = triggersb['comdict']["type"].lower()
        return triggersb

    def dictcom_load(self):
        self.dir_to_scan = botread.get_config_dirs("SpiceBot_DictComs")
        for directory in self.dir_to_scan:
            for valid_com_type in self.valid_com_types:
                poss_path = os.path.join(directory, valid_com_type)
                if os.path.exists(poss_path) and os.path.isdir(poss_path):
                    if len(os.listdir(poss_path)) > 0:
                        self.dir_to_scan.append(poss_path)

        self.valid_dictcom_dict = botread.json_to_dict(self.dir_to_scan, "Dictionary Commands", "SpiceBot_DictComs")

        for jsondict in list(self.valid_dictcom_dict.keys()):

            dict_from_file = self.valid_dictcom_dict[jsondict]

            dict_from_file["comtype"] = "dictcom"

            # default command to filename
            if "validcoms" not in list(dict_from_file.keys()):
                dict_from_file["validcoms"] = [dict_from_file["filename"]]
            elif dict_from_file["validcoms"] == []:
                dict_from_file["validcoms"] = [dict_from_file["filename"]]
            elif not isinstance(dict_from_file['validcoms'], list):
                dict_from_file["validcoms"] = [dict_from_file["validcoms"]]

            maincom = dict_from_file["validcoms"][0]

            # check for tuple dict keys and split
            validkeys = [x for x in list(dict_from_file.keys())]
            for validkey in validkeys:
                if isinstance(validkey, tuple):
                    tuple_bak = validkey
                    tuple_contents_bak = dict_from_file[validkey]
                    del dict_from_file[validkey]
                    for var in tuple_bak:
                        dict_from_file[var] = tuple_contents_bak

            # check that type is set, use cases will inherit this if not set
            if "type" not in list(dict_from_file.keys()) or dict_from_file["type"] not in self.valid_com_types:
                dict_from_file["type"] = 'simple'

            # handle basic required dict handling
            dict_from_file = self.dictcom_load_usecases(maincom, dict_from_file, self.dict_required)

            # all other keys not processed above are considered potential use cases
            otherkeys = []
            for otherkey in list(dict_from_file.keys()):
                if otherkey not in self.builtin_keys:
                    otherkeys.append(otherkey)
            if otherkeys != []:
                dict_from_file = self.dictcom_load_usecases(maincom, dict_from_file, otherkeys)

            dict_from_file["nonstockoptions"] = []
            for command in list(dict_from_file.keys()):
                if command not in prerun_shared.stockoptions:
                    dict_from_file["nonstockoptions"].append(command)

            botcommands.register(dict_from_file)

    def dictcom_load_usecases(self, maincom, dict_from_file, process_list):

        for mustbe in process_list:

            # All of the above need to be in the dict if not
            if mustbe not in list(dict_from_file.keys()):
                dict_from_file[mustbe] = dict()

            # verify if already there, that the key is a dict
            if not isinstance(dict_from_file[mustbe], dict):
                dict_from_file[mustbe] = dict()

            # Each usecase for the command must have a type, flat files inherit this type
            if "type" not in list(dict_from_file[mustbe].keys()):
                if "type" in list(dict_from_file.keys()):
                    dict_from_file[mustbe]["type"] = dict_from_file["type"]
                else:
                    dict_from_file[mustbe]["type"] = "simple"

            # each usecase needs to know if it can be updated. Default is false
            if "updates_enabled" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["updates_enabled"] = False
            if dict_from_file[mustbe]["updates_enabled"]:
                if dict_from_file[mustbe]["updates_enabled"] not in ["shared", "user"]:
                    dict_from_file[mustbe]["updates_enabled"] = "shared"

            # each usecase needs to know if it needs a target
            if "target_required" not in list(dict_from_file[mustbe].keys()):
                if dict_from_file[mustbe]["type"] in ['target', 'targetplusreason']:
                    dict_from_file[mustbe]["target_required"] = True
                else:
                    dict_from_file[mustbe]["target_required"] = False
            if "target_backup" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["target_backup"] = False
            if "target_bypass" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["target_bypass"] = []

            # special target reactions
            for reason in ['self', 'bot', 'bots', 'offline', 'unknown', 'privmsg', 'diffchannel', 'diffbot']:
                if 'react_'+reason not in list(dict_from_file[mustbe].keys()):
                    dict_from_file[mustbe]['react_'+reason] = False

            # each usecase needs to know if it needs input for fillintheblank
            if "blank_required" not in list(dict_from_file[mustbe].keys()):
                if dict_from_file[mustbe]["type"] in ['fillintheblank', 'targetplusreason', "translate"]:
                    dict_from_file[mustbe]["blank_required"] = True
                else:
                    dict_from_file[mustbe]["blank_required"] = False
            if "blank_backup" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["blank_backup"] = False
            if "blank_fail" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["blank_fail"] = ["This command requires input."]
            if not isinstance(dict_from_file[mustbe]["blank_fail"], list):
                dict_from_file[mustbe]["blank_fail"] = [dict_from_file[mustbe]["blank_fail"]]

            if "blank_phrasehandle" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["blank_phrasehandle"] = False
            if dict_from_file[mustbe]["blank_phrasehandle"]:
                if not isinstance(dict_from_file[mustbe]["blank_phrasehandle"], list):
                    dict_from_file[mustbe]["blank_phrasehandle"] = [dict_from_file[mustbe]["blank_phrasehandle"]]

            if "response_fail" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["response_fail"] = False
            if dict_from_file[mustbe]["response_fail"]:
                if not isinstance(dict_from_file[mustbe]["response_fail"], list):
                    dict_from_file[mustbe]["response_fail"] = [dict_from_file[mustbe]["response_fail"]]

            if dict_from_file[mustbe]["updates_enabled"]:
                self.adjust_nick_array(str(botconfig.nick), 'sayings', maincom + "_" + str(mustbe), dict_from_file[mustbe]["responses"], 'startup')
                dict_from_file[mustbe]["responses"] = botdb.get_plugin_value("dictcom", maincom + "_" + str(mustbe)) or []

            # each usecase needs a response
            if "responses" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["responses"] = []

            # verify responses are in list form
            if not isinstance(dict_from_file[mustbe]["responses"], list):

                # text files
                if dict_from_file[mustbe]["responses"] in list(botread.dict["text"].keys()):
                    dict_from_file[mustbe]["responses"] = botread.dict["text"][dict_from_file[mustbe]["responses"]]["lines"]

                if str(dict_from_file[mustbe]["responses"]).startswith(tuple(["https://", "http://"])):
                    botread.webpage_to_list(dict_from_file[mustbe]["responses"])
                    # TODO assign dict value, but don't load until needed
                    # TODO use botdb to store an offline version
                    if dict_from_file[mustbe]["responses"] in list(botread.dict["webpage"].keys()):
                        dict_from_file[mustbe]["responses"] = botread.dict["webpage"][dict_from_file[mustbe]["responses"]]["lines"]
                else:
                    dict_from_file[mustbe]["responses"] = [dict_from_file[mustbe]["responses"]]

            # each usecase needs a prefixtext
            if "prefixtext" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["prefixtext"] = False
            if dict_from_file[mustbe]["prefixtext"]:
                if not isinstance(dict_from_file[mustbe]["prefixtext"], list):
                    dict_from_file[mustbe]["prefixtext"] = [dict_from_file[mustbe]["prefixtext"]]

            # each usecase needs a suffixtext
            if "suffixtext" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["suffixtext"] = False
            if dict_from_file[mustbe]["suffixtext"]:
                if not isinstance(dict_from_file[mustbe]["suffixtext"], list):
                    dict_from_file[mustbe]["suffixtext"] = [dict_from_file[mustbe]["suffixtext"]]

            # Translations
            if "translations" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["translations"] = False
            if dict_from_file[mustbe]["translations"]:
                if not isinstance(dict_from_file[mustbe]["translations"], list):
                    dict_from_file[mustbe]["translations"] = [dict_from_file[mustbe]["translations"]]

            # make sure we have the smaller variation list
            if "replyvariation" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["replyvariation"] = []
            if not isinstance(dict_from_file[mustbe]["replyvariation"], list):
                dict_from_file[mustbe]["replyvariation"] = [dict_from_file[mustbe]["replyvariation"]]

            # This is to provide functionality for flat dictionaries responses
            if dict_from_file[mustbe]["responses"] == [] and mustbe == "?default":
                if "responses" in list(dict_from_file.keys()):
                    if isinstance(dict_from_file["responses"], list):
                        dict_from_file[mustbe]["responses"].extend(dict_from_file["responses"])
                    else:
                        dict_from_file[mustbe]["responses"].append(dict_from_file["responses"])
                    del dict_from_file["responses"]

            # Verify responses list is not empty
            if dict_from_file[mustbe]["responses"] == []:
                dict_from_file[mustbe]["responses"].append("No " + str(mustbe) + " responses set for " + str(maincom) + ".")

            # Some commands run query mode
            if "search_fail" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["search_fail"] = None
            if dict_from_file[mustbe]["search_fail"]:
                if not isinstance(dict_from_file[mustbe]["search_fail"], list):
                    dict_from_file[mustbe]["search_fail"] = [dict_from_file[mustbe]["search_fail"]]

            if "selection_allowed" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["selection_allowed"] = True

            # Translations
            if "randnum" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["randnum"] = False
            if dict_from_file[mustbe]["randnum"]:
                if not isinstance(dict_from_file[mustbe]["randnum"], list):
                    dict_from_file[mustbe]["randnum"] = [0, 50]
                if len(dict_from_file[mustbe]["randnum"]) == 1:
                    dict_from_file[mustbe]["randnum"] = [0, dict_from_file[mustbe]["randnum"][0]]

            if "hardcoded_channel_block" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["hardcoded_channel_block"] = []

            if "privs" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["privs"] = []

        return dict_from_file

    def adjust_nick_array(self, nick, sortingkey, usekey, values, direction):

        if not isinstance(values, list):
            values = [values]

        oldvalues = botdb.get_nick_value(nick, usekey, sortingkey) or []

        # startup entries
        if direction == 'startup':
            if oldvalues == []:
                direction == 'add'
            else:
                return

        # adjust
        for value in values:
            if direction == 'add':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction == 'startup':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction in ['del', 'remove']:
                if value in oldvalues:
                    oldvalues.remove(value)

        botdb.set_nick_value(nick, usekey, oldvalues, sortingkey)

    def setup_dictcoms(self):
        botconfig.define_section("SpiceBot_DictComs", SpiceBot_DictComs_MainSection, validate=False)

    def process(bot, trigger, botcom):

        # use the default key, unless otherwise specified
        botcom.dict["responsekey"] = "?default"


dictcoms = BotDictCommands()
