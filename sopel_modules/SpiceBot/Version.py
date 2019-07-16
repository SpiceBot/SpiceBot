# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Update system.
"""

import sopel

import requests
import json
from restkit import request
import pkg_resources

from .Config import config as botconfig


class BotVersion():

    def __init__(self):
        self.sopel = {
                    "version_local": sopel.version_info,
                    "version_local_num": sopel.__version__,
                    "version_url": 'https://sopel.chat/latest.json',
                    "version_online": None,
                    "version_online_num": None,
                    }
        self.spicebot = {
                        "version_local": None,
                        "version_local_num": None,
                        "version_url": 'https://api.github.com/users/SpiceBot/repos',
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
        self.spicebot["version_local_num"] = pkg_resources.get_distribution("sopel-modules.SpiceBot").version
        self.sopel["version_online_num"] = self.count_repo_commits()
        # get actual version number, and commit count, and assemble a version

    def count_repo_commits(self, _acc=0):
        r = request("https://api.github.com/repos/SpiceBot/SpiceBot/commits/master")
        commits = json.loads(r.body_string())
        n = len(commits)
        if n == 0:
            return _acc
        link = r.headers.get('link')
        if link is None:
            return _acc + n
        next_url = self.find_next(r.headers['link'])
        if next_url is None:
            return _acc + n
        # try to be tail recursive, even when it doesn't matter in CPython
        return self.count_repo_commits(next_url, _acc + n)

    def find_next(self, link):
        for l in link.split(','):
            a, b = l.split(';')
            if b.strip() == 'rel="next"':
                return a.strip()[1:-1]


version = BotVersion()
