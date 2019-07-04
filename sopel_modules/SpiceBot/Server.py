# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Server system.
"""

from .Config import config as botconfig


class BotServer():
    """This Logs all server values of relevance'"""
    def __init__(self):
        self.linenumber = 0
        self.dict = {
                    "host_connect": botconfig.core.host,
                    "host": botconfig.core.host,
                    }
        self.isupport = {
                        "TARGMAX": {
                                    "KICK": 1,
                                    'NOTICE': 1,
                                    'PRIVMSG': 1,
                                    },
                        }

    def rpl_welcome(self, trigger):
        self.dict["host"] = str(trigger.sender).lower()

    def parse_reply_isupport(self, trigger):

        # check against 005_Bounce
        if trigger.args[-1] != 'are supported by this server':
            return

        parameters = trigger.args[1:-1]
        for param in parameters:

            # check for value associated with the parameter
            if '=' not in param:
                self.isupport[param] = None
            else:

                key, raw_value = param.split('=')
                if ',' not in raw_value:
                    if str(raw_value).isdigit():
                        setting_value = int(raw_value)
                    self.isupport[str(key)] = raw_value
                else:

                    if str(key) not in list(self.isupport.keys()):
                        self.isupport[str(key)] = {}

                    if not isinstance(self.isupport[str(key)], dict):
                        self.isupport[str(key)] = {}

                    settings = str(raw_value).split(',')
                    for setting in settings:

                        if ":" not in setting:
                            self.isupport[str(key)][str(setting)] = None
                        else:

                            setting_name, setting_value = setting.split(":")
                            try:
                                setting_value = str(setting).split(':')[1] or None
                            except IndexError:
                                setting_value = None
                            if str(setting_value).isdigit():
                                setting_value = int(setting_value)

                            self.isupport[str(key)][str(setting_name)] = setting_value


server = BotServer()
