# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to search google"""

import sopel_modules

from .Tools import read_directory_json_to_dict

import os
from fake_useragent import UserAgent
import requests


class Sherlock():

    def __init__(self):
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.dict = {}

        dir_to_scan = []
        for plugin_dir in set(sopel_modules.__path__):
            configsdir = os.path.join(plugin_dir, "SpiceBot_Configs")
            usercfgdir = os.path.join(configsdir, "sherlock")
            dir_to_scan.append(usercfgdir)

        valid_usernames_dict = read_directory_json_to_dict(dir_to_scan, "Gif API", "SpiceBot_Gif")

        for sherlockdict in list(valid_usernames_dict.keys()):
            self.dict[sherlockdict] = valid_usernames_dict[sherlockdict]
            self.dict[sherlockdict]["cache"] = dict()

    def make_request(self, url, error_type, social_network):
        try:
            r = requests.get(url, headers=self.header)
            if r.status_code:
                return r, error_type
        except Exception as e:
            returnval = e
            returnval = None
            return returnval, ""


sherlock = Sherlock()
