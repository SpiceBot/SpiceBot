# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to read the bot's config without bot"""

from sopel.cli.run import build_parser, get_configuration

import sys
import configparser


class BotConfig():

    def __init__(self):
        self.dict = {}
        self.config = self.load_config()
        self.config_dict = self.config_file_to_dict()

    def load_config(self):
        if not len(sys.argv[1:]):
            argv = ['legacy']
        else:
            argv = sys.argv[1:]
        parser = build_parser()
        opts = parser.parse_args(argv)
        config_module = get_configuration(opts)
        return config_module

    def config_file_to_dict(self):
        configdict = dict()
        config = configparser.ConfigParser()
        config.read(self.config.filename)
        for each_section in config.sections():
            if each_section not in configdict.keys():
                configdict[each_section] = dict()
                for (each_key, each_val) in config.items(each_section):
                    if each_key not in configdict[each_section].keys():
                        configdict[each_section][each_key] = each_val
        return configdict


botconfig = BotConfig()
