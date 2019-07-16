# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Update system.
"""

import sopel
from sopel.config.types import StaticSection, ValidatedAttribute

import requests

from .Config import config as botconfig


class SpiceBot_Update_MainSection(StaticSection):
    gitrepo = ValidatedAttribute('gitrepo', default="https://github.com/SpiceBot/SpiceBot")
    gitbranch = ValidatedAttribute('gitbranch', default="master")


class BotUpdates():

    def __init__(self):
        self.sopel = {
                    "version_local": sopel.version_info,
                    "version_url": 'https://sopel.chat/latest.json',
                    "version_online": None,
                    }
        self.spicebot = False

        self.check_sopel()

    def check_sopel(self):
        info = requests.get(self.sopel["version_url"], verify=botconfig.core.verify_ssl).json()
        if self.sopel["version_local"].releaselevel == 'final':
            latest = info['version']
        else:
            latest = info['unstable']

        self.sopel["version_online"] = sopel._version_info(latest)

    def check_spicebot(self):
        return
        self.sopel = True


version = BotUpdates()
