# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""A way to search google"""

import urllib
import requests
from fake_useragent import UserAgent

from sopel.config.types import StaticSection, ValidatedAttribute

from .Config import config as botconfig

# TODO add a cache flush


class SpiceBot_Google_MainSection(StaticSection):
    search_api = ValidatedAttribute('search_api', default=None)


class Google():

    def __init__(self):
        self.setup_google()
        self.cache = {
                    "info": {},
                    "maps": {}
                    }

    def setup_google(self):
        botconfig.define_section("SpiceBot_Google", SpiceBot_Google_MainSection, validate=False)

    def search(self, searchterm, searchtype="info"):

        # losercase searching
        searchterm = searchterm.lower()

        """
        safe='off',
        """

        # check cache
        if searchtype not in list(self.cache.keys()):
            self.cache[searchtype] = dict()
        if searchterm in self.cache[searchtype]:
            return self.cache[searchtype][searchterm]

        if searchtype == 'maps':
            returnurl = self.search_maps(searchterm)
        elif searchtype == 'youtube':
            returnurl = self.search_youtube(searchterm)
        else:
            returnurl = self.search_info(searchterm)

        if returnurl:
            self.cache[searchtype][searchterm] = str(returnurl)
        return returnurl

    def search_info(self, searchterm, retry=False):
        header = {'User-Agent': str(UserAgent().chrome)}
        data = searchterm.replace(' ', '+')
        lookfor = data.replace(':', '%3A')
        if not botconfig.SpiceBot_Google.search_api or retry:
            try:
                var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI', headers=header)
            except Exception as e:
                var = e
                var = None
            if not var or not var.url:
                return None
            return var.url
        else:
            return self.search_info(searchterm, retry=True)

    def search_maps(self, searchterm, retry=False):
        header = {'User-Agent': str(UserAgent().chrome)}
        data = searchterm.replace(' ', '+')
        lookfor = data.replace(':', '%3A')
        if not botconfig.SpiceBot_Google.search_api or retry:
            try:
                var = requests.get(r'http://www.google.com/maps/place/' + lookfor, headers=header)
            except Exception as e:
                var = e
                var = None
            if not var or not var.url:
                return None
            return var.url
        else:
            return self.search_maps(searchterm, retry=True)

    def search_youtube(self, searchterm, retry=False):
        header = {'User-Agent': str(UserAgent().chrome)}
        data = searchterm.replace(' ', '+')
        lookfor = data.replace(':', '%3A')
        if not botconfig.SpiceBot_Google.search_api or retry:
            try:
                var = requests.get(r'https://www.youtube.com/search?q=' + lookfor + '&btnI', headers=header)
            except Exception as e:
                var = e
                var = None
            if not var or not var.url:
                return None
            return var.url
        else:
            return self.search_youtube(searchterm, retry=True)


google = Google()
