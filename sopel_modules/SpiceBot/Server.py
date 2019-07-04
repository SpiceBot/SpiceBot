# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Server system.
"""

from .Config import config as botconfig


class BotServer():
    """This Logs all server values of relevance'"""
    def __init__(self):
        self.dict = {
                    "host_connect": botconfig.core.host,
                    "host": botconfig.core.host,
                    }

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        """We will try to find a dict value, or return None"""
        if name.lower() in list(self.dict.keys()):
            return self.dict[str(name).lower()]
        else:
            raise Exception('Server dict does not contain a function or key ' + str(name.lower()))


server = BotServer()
