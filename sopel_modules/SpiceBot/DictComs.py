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

import requests
from fake_useragent import UserAgent
import urllib


class SpiceBot_DictComs_MainSection(StaticSection):
    extra = ListAttribute('extra')


class BotDictCommands():

    def __init__(self):
        self.setup_dictcoms()
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.valid_com_types = [
                                'simple', 'fillintheblank', 'targetplusreason',
                                'sayings', "readfromfile", "readfromurl",
                                "ascii_art", "gif", "translate", "responses",
                                "feeds", "search"
                                ]

        self.dir_to_scan = botread.get_config_dirs("SpiceBot_DictComs")

        self.valid_dictcom_dict = botread.json_to_dict(self.dir_to_scan, "Dictionary Commands", "SpiceBot_DictComs")

        for jsondict in list(self.valid_dictcom_dict.keys()):

            dict_from_file = self.valid_dictcom_dict[jsondict]

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

            dict_from_file["comtype"] = "prefix_" + dict_from_file["type"]

            # Don't process these.
            keysprocessed = []
            keysprocessed.extend(["validcoms", "filepath", "filename", "comtype"])
            keysprocessed.extend(["author", "contributors"])
            keysprocessed.extend(["validcoms", "filepath", "filename", "description", "exampleresponse", "example", "privs"])

            # handle basic required dict handling
            dict_required = ["?default"]
            dict_from_file = self.bot_dict_use_cases(maincom, dict_from_file, dict_required)
            keysprocessed.extend(dict_required)

            # remove later
            keysprocessed.append("type")

            # all other keys not processed above are considered potential use cases
            otherkeys = []
            for otherkey in list(dict_from_file.keys()):
                if otherkey not in keysprocessed:
                    otherkeys.append(otherkey)
            if otherkeys != []:
                dict_from_file = self.bot_dict_use_cases(maincom, dict_from_file, otherkeys)
            keysprocessed.extend(otherkeys)

            botcommands.register(dict_from_file)

    def bot_dict_use_cases(self, maincom, dict_from_file, process_list):

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

            # if dict_from_file[mustbe]["updates_enabled"]:
            #    adjust_nick_array(bot, str(bot.nick), 'long', 'sayings', maincom + "_" + str(mustbe), dict_from_file[mustbe]["responses"], 'startup')
            #    dict_from_file[mustbe]["responses"] = get_nick_value(bot, str(bot.nick), 'long', 'sayings', maincom + "_" + str(mustbe)) or []

            # each usecase needs a response
            if "responses" not in list(dict_from_file[mustbe].keys()):
                dict_from_file[mustbe]["responses"] = []

            # verify responses are in list form
            if not isinstance(dict_from_file[mustbe]["responses"], list):
                # TODO read text files
                # if dict_from_file[mustbe]["responses"] in bot.memory["botdict"]["tempvals"]['txt_files'].keys():
                #    dict_from_file[mustbe]["responses"] = bot.memory["botdict"]["tempvals"]['txt_files'][dict_from_file[mustbe]["responses"]]
                if str(dict_from_file[mustbe]["responses"]).startswith(tuple(["https://", "http://"])):
                    try:
                        page = requests.get(dict_from_file[mustbe]["responses"], headers=self.header)
                    except Exception as e:
                        page = e
                        page = None

                    if page and not str(page.status_code).startswith(tuple(["4", "5"])):
                        htmlfile = urllib.request.urlopen(dict_from_file[mustbe]["responses"])
                        lines = htmlfile.read().splitlines()
                        dict_from_file[mustbe]["responses"] = lines
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

    def setup_dictcoms(self):
        botconfig.define_section("SpiceBot_DictComs", SpiceBot_DictComs_MainSection, validate=False)


dictcoms = BotDictCommands()
