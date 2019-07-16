# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Update system.
"""

import sopel

import requests
import feedparser
import pkg_resources
from fake_useragent import UserAgent
import urllib

from .Config import config as botconfig


class BotVersion():

    def __init__(self):
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.sopel = {
                    "version_local": sopel.version_info,
                    "version_local_num": sopel.__version__,
                    "version_url": 'https://sopel.chat/latest.json',
                    "version_online": None,
                    "version_online_num": None,
                    }
        self.spicebot = {
                        "version_local": None,
                        "version_local_num": pkg_resources.get_distribution("sopel-modules.SpiceBot").version,
                        "version_url": "https://api.github.com/repos/SpiceBot/SpiceBot/commits/master",
                        "version_online": None,
                        "version_online_num": None,
                        }

        self.check_sopel()
        self.check_spicebot()

    def check_sopel(self):
        info = requests.get(self.sopel["version_url"], verify=botconfig.core.verify_ssl).json()
        if self.sopel["version_local"].releaselevel == 'final':
            self.sopel["version_online_num"] = info['version']
            self.sopel["notes"] = info['release_notes']
        else:
            self.sopel["version_online_num"] = info['unstable']
            self.sopel["notes"] = info.get('unstable_notes', '')
            if self.sopel["notes"]:
                self.sopel["notes"] = 'Full release notes at ' + self.sopel["notes"]

        self.sopel["version_online"] = sopel._version_info(self.sopel["version_online_num"])

    def check_spicebot(self):

        htmlfile = urllib.request.urlopen("https://raw.githubusercontent.com/SpiceBot/SpiceBot/master/setup.py")
        lines = htmlfile.read().splitlines()
        self.spicebot["version_online_num"] = self.spicebot["version_local_num"]
        for line in lines:
            if "version=" in line:
                line = line.replace("version=", '')
                line = line.replace("'", '')
                self.spicebot["version_online_num"] = line
                continue

        feedjson = feedparser.parse("https://github.com/SpiceBot/SpiceBot/commits/master.atom")
        self.spicebot["version_online_num"] = str(self.spicebot["version_online_num"]) + "." + str(len(feedjson.entries))


version = BotVersion()
