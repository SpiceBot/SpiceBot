# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""This is a method to read files, online and local, and cache them"""

import sopel_modules

import os
import codecs
import requests
import urllib
from fake_useragent import UserAgent

from .Logs import logs
from .Config import config as botconfig
from .Tools import prerun_shared


class BotRead():

    def __init__(self):
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.dict = {
                    "text": {},
                    "webpage": {},
                    }
        self.load_txt_files()

    def load_txt_files(self):
        dir_to_scan = []
        for plugin_dir in set(sopel_modules.__path__):
            textdir = os.path.join(plugin_dir, "SpiceBot_Text")
            if os.path.exists(textdir) and os.path.isdir(textdir):
                if len(os.listdir(textdir)) > 0:
                    dir_to_scan.append(textdir)
        # iterate over files within
        for directory in dir_to_scan:
            for txtfile in os.listdir(directory):
                text_file_list = []
                text_file = open(os.path.join(directory, txtfile), 'r')
                lines = text_file.readlines()
                for line in lines:
                    text_file_list.append(line)
                text_file.close()
                self.dict["text"][txtfile] = {
                                                "lines": text_file_list
                                                }

    def webpage_to_list(self, url):
        try:
            page = requests.get(url, headers=self.header)
        except Exception as e:
            page = e
            page = None

        if page and not str(page.status_code).startswith(tuple(["4", "5"])):
            htmlfile = urllib.request.urlopen(url)
            lines = htmlfile.read().splitlines()
            self.dict["webpage"][url] = {
                                        "lines": lines
                                        }

    def get_config_dirs(self, config_dir_name):
        dir_to_scan = []

        # check config directory stored within this project
        for plugin_dir in set(sopel_modules.__path__):
            configsdir = os.path.join(plugin_dir, "SpiceBot_Configs")
            cfgdir = os.path.join(configsdir, config_dir_name)
            if os.path.exists(cfgdir) and os.path.isdir(cfgdir):
                if len(os.listdir(cfgdir)) > 0:
                    dir_to_scan.append(cfgdir)

        # attempt to check for extra directories
        try:
            extradir = botconfig.extra
            extradir = eval("botconfig." + config_dir_name + ".extra")
        except Exception as e:
            extradir = e
            extradir = []
        if len(extradir):
            for extracfgdir in extradir:
                if os.path.exists(extracfgdir) and os.path.isdir(extracfgdir):
                    if len(os.listdir(extracfgdir)) > 0:
                        dir_to_scan.append(extracfgdir)

        return dir_to_scan

    def json_to_dict(self, directories, configtypename="Config File", log_from='read_directory_json_to_dict', logging=True):

        if not isinstance(directories, list):
            directories = [directories]

        configs_dict = {}
        filesprocess, fileopenfail, filecount = [], 0, 0
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                if len(os.listdir(directory)) > 0:
                    for file in os.listdir(directory):
                        filepath = os.path.join(directory, file)
                        if os.path.isfile(filepath) and filepath.endswith('.json'):
                            filesprocess.append(filepath)

        for filepath in filesprocess:

            # Read dictionary from file, if not, enable an empty dict
            filereadgood = True
            try:
                inf = codecs.open(filepath, "r", encoding='utf-8')
                infread = inf.read()
                # Close File
                inf.close()
                dict_from_file = eval(infread)
            except Exception as e:
                filereadgood = False
                if logging:
                    logs.log(log_from, "Error loading %s: %s (%s)" % (configtypename, e, filepath))
                dict_from_file = dict()

            # gather file stats
            slashsplit = str(filepath).split("/")
            filename = slashsplit[-1]
            filename_base = os.path.basename(filename).rsplit('.', 1)[0]

            if not filereadgood or not isinstance(dict_from_file, dict):
                fileopenfail += 1
            else:
                filecount += 1
                dict_from_file["filepath"] = str(filepath)
                dict_from_file["filename"] = str(filename_base)
                dict_from_file["folderpath"] = dict_from_file["filepath"].split("/" + dict_from_file["filename"])[0]
                dict_from_file["foldername"] = str(dict_from_file["folderpath"]).split("/")[-1]
                dict_from_file = self.command_defaults(dict_from_file)
                configs_dict[filename_base] = dict_from_file

        if filecount:
            if logging:
                logs.log(log_from, 'Registered %d %s dict files,' % (filecount, configtypename))
                logs.log(log_from, '%d %s dict files failed to load' % (fileopenfail, configtypename), True)
        else:
            if logging:
                logs.log(log_from, "Warning: Couldn't load any %s dict files" % (configtypename))

        return configs_dict

    def json_to_dict_simple(self, directories, configtypename="Config File", log_from='read_directory_json_to_dict', logging=True):

        if not isinstance(directories, list):
            directories = [directories]

        configs_dict = {}
        filesprocess, fileopenfail, filecount = [], 0, 0
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                if len(os.listdir(directory)) > 0:
                    for file in os.listdir(directory):
                        filepath = os.path.join(directory, file)
                        if os.path.isfile(filepath) and filepath.endswith('.json'):
                            filesprocess.append(filepath)

        for filepath in filesprocess:

            # Read dictionary from file, if not, enable an empty dict
            filereadgood = True
            try:
                inf = codecs.open(filepath, "r", encoding='utf-8')
                infread = inf.read()
                # Close File
                inf.close()
                dict_from_file = eval(infread)
            except Exception as e:
                filereadgood = False
                if logging:
                    logs.log(log_from, "Error loading %s: %s (%s)" % (configtypename, e, filepath))
                dict_from_file = dict()

            # gather file stats
            slashsplit = str(filepath).split("/")
            filename = slashsplit[-1]
            filename_base = os.path.basename(filename).rsplit('.', 1)[0]

            if not filereadgood or not isinstance(dict_from_file, dict):
                fileopenfail += 1
            else:
                filecount += 1
                dict_from_file["filepath"] = str(filepath)
                dict_from_file["filename"] = str(filename_base)
                dict_from_file["folderpath"] = dict_from_file["filepath"].split("/" + dict_from_file["filename"])[0]
                dict_from_file["foldername"] = str(dict_from_file["folderpath"]).split("/")[-1]
                # dict_from_file = self.command_defaults(dict_from_file)
                configs_dict[filename_base] = dict_from_file

        if filecount:
            if logging:
                logs.log(log_from, 'Registered %d %s dict files,' % (filecount, configtypename))
                logs.log(log_from, '%d %s dict files failed to load' % (fileopenfail, configtypename), True)
        else:
            if logging:
                logs.log(log_from, "Warning: Couldn't load any %s dict files" % (configtypename))

        return configs_dict

    def module_json_to_dict(self, filepath, logging=True):

        # gather file stats
        slashsplit = str(filepath).split("/")
        filename = slashsplit[-1]
        filename_base = os.path.basename(filename).rsplit('.', 1)[0]
        folderpath = str(filepath).split("/" + filename)[0]

        jsonpath = os.path.join(folderpath, filename_base + ".json")
        if os.path.exists(jsonpath) and os.path.isfile(jsonpath):

            # Read dictionary from file, if not, enable an empty dict
            filereadgood = True
            try:
                inf = codecs.open(jsonpath, "r", encoding='utf-8')
                infread = inf.read()
                dict_from_file = eval(infread)
                # Close File
                inf.close()
            except Exception as e:
                filereadgood = False
                if logging:
                    logs.log("SpiceBot_Modules", "Error loading %s: %s (%s)" % ("Module Commands", e, jsonpath))
                dict_from_file = dict()

            # gather file stats
            slashsplit = str(filepath).split("/")
            filename = slashsplit[-1]
            filename_base = os.path.basename(filename).rsplit('.', 1)[0]

            if not filereadgood or not isinstance(dict_from_file, dict):
                dict_from_file = {}
            else:
                dict_from_file["filepath"] = str(jsonpath)
                dict_from_file["filename"] = str(filename_base)
                dict_from_file["folderpath"] = dict_from_file["filepath"].split("/" + dict_from_file["filename"])[0]
                dict_from_file["foldername"] = str(dict_from_file["folderpath"]).split("/")[-1]
                dict_from_file = self.command_defaults(dict_from_file)
        else:
            dict_from_file = {}

        dict_from_file = self.command_defaults(dict_from_file)
        return dict_from_file

    def command_defaults(self, dict_from_file):

        # the command must have an author
        if "author" not in list(dict_from_file.keys()):
            dict_from_file["author"] = "deathbybandaid"

        # the command must have a contributors list
        if "contributors" not in list(dict_from_file.keys()):
            dict_from_file["contributors"] = []
        if not isinstance(dict_from_file["contributors"], list):
            dict_from_file["contributors"] = [dict_from_file["contributors"]]
        if "deathbybandaid" not in dict_from_file["contributors"]:
            dict_from_file["contributors"].append("deathbybandaid")
        if dict_from_file["author"] not in dict_from_file["contributors"]:
            dict_from_file["contributors"].append(dict_from_file["author"])

        if "example" not in list(dict_from_file.keys()):
            dict_from_file["example"] = "$maincom"
            # TODO
            # if dict_from_file["comtype"] == "nickname":
            #    dict_from_file["example"] = str(botconfig.nick + " $maincom")
            # else:
            #    dict_from_file["example"] = str(botconfig.core.prefix_list[0] + "$maincom")
        if not dict_from_file["example"].startswith("$maincom"):
            dict_from_file["example"] = "$maincom " + dict_from_file["example"]

        if "exampleresponse" not in list(dict_from_file.keys()):
            dict_from_file["exampleresponse"] = None

        if "description" not in list(dict_from_file.keys()):
            dict_from_file["description"] = None

        if "privs" not in list(dict_from_file.keys()):
            dict_from_file["privs"] = []

        if "hardcoded_channel_block" not in list(dict_from_file.keys()):
            dict_from_file["hardcoded_channel_block"] = []

        # check that type is set, use cases will inherit this if not set
        if "type" not in list(dict_from_file.keys()):
            dict_from_file["type"] = dict_from_file["foldername"]

        dict_from_file["nonstockoptions"] = ["?default"]
        for command in list(dict_from_file.keys()):
            if command not in prerun_shared.stockoptions:
                dict_from_file["nonstockoptions"].append(command)

        ignorelist = []
        if dict_from_file["type"] == "SpiceBot_Gif":
            ignorelist.extend(["url", "query", "limit", "id", "api_id", "key", "nsfw", "sfw", "sfw", "results", "cururl", "additional_url"])
        elif dict_from_file["type"] == "SpiceBot_Search":
            ignorelist.extend(["url", "query", "additional_url"])
        elif dict_from_file["type"] == "SpiceBot_Sherlock":
            ignorelist.extend(["url", "errorType", "errorMsg", "noPeriod", "errorUrl"])

        for ignoreitem in ignorelist:
            if ignoreitem in dict_from_file["nonstockoptions"]:
                dict_from_file["nonstockoptions"].remove(ignoreitem)

        for specialcase in dict_from_file["nonstockoptions"]:

            # All of the above need to be in the dict if not
            if specialcase not in list(dict_from_file.keys()):
                dict_from_file[specialcase] = dict()

            # verify if already there, that the key is a dict
            if not isinstance(dict_from_file[specialcase], dict):
                dict_from_file[specialcase] = dict()

            if "responses" not in list(dict_from_file[specialcase].keys()):
                dict_from_file[specialcase]["responses"] = []

            if "type" not in list(dict_from_file[specialcase].keys()):
                dict_from_file[specialcase]["type"] = "module"

            # each usecase needs to know if it can be updated. Default is false
            if "updates_enabled" not in list(dict_from_file[specialcase].keys()):
                dict_from_file[specialcase]["updates_enabled"] = False
            if dict_from_file[specialcase]["updates_enabled"]:
                if dict_from_file[specialcase]["updates_enabled"] not in ["shared", "user"]:
                    dict_from_file[specialcase]["updates_enabled"] = "shared"

            if "selection_allowed" not in list(dict_from_file[specialcase].keys()):
                dict_from_file[specialcase]["selection_allowed"] = True

        if "?default" in dict_from_file["nonstockoptions"]:
            dict_from_file["nonstockoptions"].remove("?default")

        return dict_from_file


read = BotRead()
