# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to read the bot's config without bot"""

from sopel.cli.run import build_parser, get_configuration

import sys
import configparser


class BotConfig():

    def __init__(self):
        self.dict = {}
        self.config = None
        self.filename = None
        self.load_config()

    def load_config(self):

        # Load config
        parser = build_parser()
        if not len(sys.argv[1:]):
            argv = ['legacy']
        else:
            argv = sys.argv[1:]
        opts = parser.parse_args(argv)
        self.config = get_configuration(opts)

        # Filename
        self.filename = self.config.filename

        # load as dict
        self.dict = self.config_file_to_dict()

    def config_file_to_dict(self):
        configdict = dict()
        config = configparser.ConfigParser()
        config.read(self.filename)
        for each_section in config.sections():
            if each_section not in configdict.keys():
                configdict[each_section] = dict()
                for (each_key, each_val) in config.items(each_section):
                    if each_key not in configdict[each_section].keys():
                        configdict[each_section][each_key] = each_val
        return configdict


botconfig = BotConfig()
