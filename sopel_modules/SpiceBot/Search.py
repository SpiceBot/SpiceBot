# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to search on the internet"""

import requests
import urllib
from fake_useragent import UserAgent

from sopel.config.types import StaticSection, ValidatedAttribute

from .Config import config as botconfig

# TODO add a cache flush


class SpiceBot_Search_MainSection(StaticSection):
    search_api = ValidatedAttribute('search_api', default=None)


class Search():

    def __init__(self):
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.setup_search()
        self.cache = {
                    "info": {},
                    "maps": {},
                    "youtube": {},
                    "spiceworks": {},
                    }

    def setup_search(self):
        botconfig.define_section("SpiceBot_Search", SpiceBot_Search_MainSection, validate=False)

    def search(self, searchdict):

        # list of defaults
        query_defaults = {
                        "query": None,
                        "query_type": "info",
                        "query_url": None
                        }

        # set defaults if they don't exist
        for key in query_defaults:
            if key not in list(searchdict.keys()):
                searchdict[key] = query_defaults[key]

        # Replace spaces in search query
        searchdict["searchquery"] = urllib.request.pathname2url(searchdict["query"])

        """
        safe='off',
        """

        # check cache
        if searchdict["query_type"] not in list(self.cache.keys()):
            self.cache[searchdict["query_type"]] = dict()
        if searchdict["query_type"] != "custom":
            if searchdict["query"].lower() in self.cache[searchdict["query_type"]]:
                return self.cache[searchdict["query_type"]][searchdict["query"]]

        if searchdict["query_type"] == 'maps':
            returnurl = self.search_maps_google(searchdict)
        elif searchdict["query_type"] == 'youtube':
            returnurl = self.search_youtube(searchdict)
        elif searchdict["query_type"] == 'custom':
            returnurl = self.search_info_custom(searchdict)
        else:
            returnurl = self.search_info_google(searchdict)

        if returnurl and searchdict["query_type"] != 'custom':
            self.cache[searchdict["query_type"]][searchdict["query"].lower()] = str(returnurl)

        return returnurl

    def search_info_custom(self, searchdict):
        lookfor = searchdict["searchquery"]
        try:
            var = requests.get(r'' + searchdict["query_url"] + lookfor, headers=self.header)
        except Exception as e:
            var = e
            var = None
        if not var or not var.url:
            return None
        return var.url

    def search_info_google(self, searchdict, retry=False):
        lookfor = searchdict["searchquery"]
        if not botconfig.SpiceBot_Google.search_api or retry:
            try:
                var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI', headers=self.header)
            except Exception as e:
                var = e
                var = None
            if not var or not var.url:
                return None
            return var.url
        else:
            return self.search_info_google(searchdict, retry=True)

    def search_maps_google(self, searchdict, retry=False):
        lookfor = searchdict["searchquery"]
        if not botconfig.SpiceBot_Google.search_api or retry:
            try:
                var = requests.get(r'http://www.google.com/maps/place/' + lookfor, headers=self.header)
            except Exception as e:
                var = e
                var = None
            if not var or not var.url:
                return None
            return var.url
        else:
            return self.search_maps_google(searchdict, retry=True)

    def search_youtube(self, searchdict, retry=False):
        lookfor = searchdict["searchquery"]
        if not botconfig.SpiceBot_Google.search_api or retry:
            try:
                var = requests.get(r'https://www.youtube.com/search?q=' + lookfor + '&btnI', headers=self.header)
            except Exception as e:
                var = e
                var = None
            if not var or not var.url:
                return None
            return var.url
        else:
            return self.search_youtube(searchdict, retry=True)


search = Search()
