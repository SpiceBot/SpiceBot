# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""This is a method to read files, online and local, and cache them"""

import sopel_modules

import os
import codecs

from .Logs import logs


class BotRead():

    def __init__(self):
        self.dict = dict()

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
            inf = codecs.open(filepath, "r", encoding='utf-8')
            infread = inf.read()
            try:
                dict_from_file = eval(infread)
            except Exception as e:
                filereadgood = False
                if logging:
                    logs.log(log_from, "Error loading %s: %s (%s)" % (configtypename, e, filepath))
                dict_from_file = dict()
            # Close File
            inf.close()

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
                configs_dict[filename_base] = dict_from_file

        if filecount:
            if logging:
                logs.log(log_from, 'Registered %d %s dict files,' % (filecount, configtypename))
                logs.log(log_from, '%d %s dict files failed to load' % (fileopenfail, configtypename), True)
        else:
            if logging:
                logs.log(log_from, "Warning: Couldn't load any %s dict files" % (configtypename))

        return configs_dict


read = BotRead()
