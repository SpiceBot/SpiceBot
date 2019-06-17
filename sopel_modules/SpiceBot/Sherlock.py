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

    def check_network(self, username, social_network):

        if username in self.dict[social_network]["cache"]:
            return True

        url = self.dict.get(social_network).get("url").format(username)
        error_type = self.dict.get(social_network).get("errorType")
        cant_have_period = self.dict.get(social_network).get("noPeriod")

        if ("." in username) and (cant_have_period == "True"):
            while ("." in username):
                username = username.replace(".", '')

        r, error_type = self.make_request(url=url, error_type=error_type, social_network=social_network)

        user_exists = True

        if error_type == "message":
            error = self.dict.get(social_network).get("errorMsg")
            # Checks if the error message is in the HTML
            if error in r.text:
                user_exists = False

        elif error_type == "status_code":
            # Checks if the status code of the repsonse is 404
            if r.status_code == 404:
                user_exists = False

        elif error_type == "response_url":
            error = self.dict.get(social_network).get("errorUrl")
            # Checks if the redirect url is the same as the one defined in data.json
            if error in r.url:
                user_exists = False

        if user_exists:
            self.dict[social_network]["cache"].append(username)
            return True
        else:
            return False

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
