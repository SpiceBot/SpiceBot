# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to read the bot's config without bot"""

from sopel.cli.run import build_parser, get_configuration

import sys


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

    def define_section(self, name, cls_, validate=True):
        return self.config.define_section(name, cls_, validate)

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        """We will try to find a core value, or return None"""
        if hasattr(self.config, name):
            return eval("self.config.core." + name)
        else:
            return None


config = BotConfig()
