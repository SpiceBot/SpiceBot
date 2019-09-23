# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to search on the internet"""

import requests
import urllib
from fake_useragent import UserAgent

from sopel.config.types import StaticSection, ValidatedAttribute

from .Config import config as botconfig
from .Read import read as botread
from .Commands import commands as botcommands

from .Logs import logs

# TODO add a cache flush


class SpiceBot_Search_MainSection(StaticSection):
    search_api = ValidatedAttribute('search_api', default=None)


class Search():

    def __init__(self):
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.setup_search()
        self.dir_to_scan = botread.get_config_dirs("SpiceBot_Search")
        valid_search_api_dict = botread.json_to_dict_simple(self.dir_to_scan, "Search API", "SpiceBot_Search")
        self.valid_api = {}

        self.cache = {}

        for search_api in list(valid_search_api_dict.keys()):

            self.valid_api[search_api] = valid_search_api_dict[search_api]
            self.valid_api[search_api]["apikey"] = None
            self.valid_api[search_api]["cache"] = dict()

            self.valid_api[search_api]["comtype"] = "search_prefix"
            self.valid_api[search_api]["validcoms"] = [self.valid_api[search_api]["filename"]]
            botcommands.register(self.valid_api[search_api])

            # check cache
            if search_api not in list(self.cache.keys()):
                self.cache[search_api] = dict()

    def setup_search(self):
        botconfig.define_section("SpiceBot_Search", SpiceBot_Search_MainSection, validate=False)

    def search(self, searchdict):

        # list of defaults
        query_defaults = {
                        "query": '',
                        "query_type": "google",
                        "nsfw": False,
                        }

        # set defaults if they don't exist
        for key in query_defaults:
            if key not in list(searchdict.keys()):
                searchdict[key] = query_defaults[key]
        for key in list(self.valid_api[searchdict["query_type"]].keys()):
            if key not in list(searchdict.keys()):
                searchdict[key] = self.valid_api[searchdict["query_type"]][key]

        # Replace spaces in search query
        searchdict["searchquery"] = urllib.request.pathname2url(searchdict["query"])

        """
        safe='off',
        """

        # check cache
        if searchdict["query_type"] not in list(self.cache.keys()):
            self.cache[searchdict["query_type"]] = dict()

        if searchdict["query"].lower() in self.cache[searchdict["query_type"]]:
            return self.cache[searchdict["query_type"]][searchdict["query"]]

        searchdict["searchurl"] = self.search_url_assemble(searchdict)
        returnurl = self.search_handler(searchdict)

        if returnurl:
            self.cache[searchdict["query_type"]][searchdict["query"].lower()] = str(returnurl)

        return returnurl

    def search_handler(self, searchdict):
        try:
            results = requests.get(searchdict["searchurl"], headers=self.header).text()
        except Exception as e:
            results = e
            logs.log('SpiceBot_Search', str(e))
            return None
        logs.log('SpiceBot_Search', str(results))
        return None

    def search_handler_old(self, searchdict):
        try:
            var = requests.get(searchdict["searchurl"], headers=self.header)
        except Exception as e:
            var = e
            var = None
        if not var or not var.url:
            return None
        return var.url

    def search_url_assemble(self, searchdict):
        # url base
        url = str(searchdict["url"])
        # query
        url += str(self.valid_api[searchdict["query_type"]]["query_param"]) + str(searchdict["query"])
        # nsfw search? TODO
        # additional parts
        if "additional_url" in list(self.valid_api[searchdict["query_type"]].keys()):
            url += str(self.valid_api[searchdict["query_type"]]['additional_url'])
        return url


search = Search()
