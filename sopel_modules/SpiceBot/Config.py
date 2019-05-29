# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to read the bot's config without bot"""

from sopel.cli.run import build_parser, get_configuration

import sys
import configparser


class BotConfig():

    def __init__(self):
        self.dict = {}

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
        config = configparser.ConfigParser()
        config.read(self.filename)
        for each_section in config.sections():
            if each_section.lower() not in self.dict.keys():
                self.dict[each_section.lower()] = dict()
            for (each_key, each_val) in config.items(each_section):
                if each_key.lower() not in self.dict[each_section.lower()].keys():
                    self.dict[each_section.lower()][each_key.lower()] = each_val

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        """We will try to find a core value, or return None"""
        if name.lower() in self.dict["core"].keys():
            return self.dict["core"][str(name).lower()]
        else:
            return None


config = BotConfig()
