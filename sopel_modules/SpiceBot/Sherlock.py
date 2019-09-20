# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to search for usernames"""

from sopel.config.types import StaticSection, ListAttribute

from .Read import read as botread
from .Config import config as botconfig

from fake_useragent import UserAgent
import requests
import time


class SpiceBot_Sherlock_MainSection(StaticSection):
    extra = ListAttribute('extra')


class Sherlock():

    def __init__(self):
        self.setup_sherlock()
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.dict = {}

        dir_to_scan = botread.get_config_dirs("SpiceBot_Sherlock")

        valid_usernames_dict = botread.json_to_dict(dir_to_scan, "Sherlock", "SpiceBot_Sherlock")

        for social_network in list(valid_usernames_dict.keys()):
            self.dict[social_network] = valid_usernames_dict[social_network]
            self.dict[social_network]["cache"] = dict()

    def setup_sherlock(self):
        botconfig.define_section("SpiceBot_Sherlock", SpiceBot_Sherlock_MainSection, validate=False)

    def check_network(self, username, social_network):
        username = str(username).lower()

        if username in list(self.dict[social_network]["cache"].keys()):
            if time.time() - self.dict[social_network]["cache"][username]["time"] <= 1800:
                return self.dict[social_network]["cache"][username]["exists"]
        else:
            self.dict[social_network]["cache"][username] = dict()

        url = self.dict.get(social_network).get("url").format(username)
        error_type = self.dict.get(social_network).get("errorType")
        cant_have_period = self.dict.get(social_network).get("noPeriod")

        if ("." in username) and (cant_have_period == "True"):
            while ("." in username):
                username = username.replace(".", '')

        r, error_type = self.make_request(url=url, error_type=error_type, social_network=social_network)

        user_exists = False

        if error_type == "message":
            error = self.dict.get(social_network).get("errorMsg")
            # Checks if the error message is in the HTML
            if error not in r.text:
                user_exists = True

        elif error_type == "status_code":
            # Checks if the status code of the repsonse is 404
            if not r.status_code == 404:
                user_exists = True

        elif error_type == "response_url":
            error = self.dict.get(social_network).get("errorUrl")
            # Checks if the redirect url is the same as the one defined in data.json
            if error not in r.url:
                user_exists = True

        self.dict[social_network]["cache"][username] = {
                                                        "time": time.time(),
                                                        "exists": user_exists
                                                        }

        if user_exists:
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
