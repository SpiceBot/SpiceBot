# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""How to handle gifs"""

from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute

from .Config import config as botconfig
from .Read import read as botread
from .Commands import commands as botcommands

import spicemanip

from fake_useragent import UserAgent
import urllib
import random
import requests
import json


class SpiceBot_Gif_MainSection(StaticSection):
    extra = ListAttribute('extra')
    nsfw = ValidatedAttribute('nsfw', default=False)


class GifAPISection(StaticSection):
    apikey = ValidatedAttribute('apikey', default=None)


class BotGif():

    def __init__(self):
        self.setup_gif()
        self.badlinks = []
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.valid_api = {}

        self.dir_to_scan = botread.get_config_dirs("SpiceBot_Gif")

        valid_gif_api_dict = botread.json_to_dict(self.dir_to_scan, "Gif API", "SpiceBot_Gif")

        for gif_api in list(valid_gif_api_dict.keys()):
            botconfig.define_section(gif_api, GifAPISection, validate=False)

            self.valid_api[gif_api] = valid_gif_api_dict[gif_api]
            self.valid_api[gif_api]["apikey"] = None
            self.valid_api[gif_api]["cache"] = dict()

            apikey = eval("botconfig." + gif_api + ".apikey")
            if apikey:
                self.valid_api[gif_api]["apikey"] = apikey

            self.valid_api[gif_api]["comtype"] = "gif_prefix"
            self.valid_api[gif_api]["validcoms"] = [self.valid_api[gif_api]["filename"]]
            botcommands.register(self.valid_api[gif_api])

    def setup_gif(self):
        botconfig.define_section("SpiceBot_Gif", SpiceBot_Gif_MainSection, validate=False)

    def get_gif(self, searchdict):

        # list of defaults
        query_defaults = {
                        "query": None,
                        "searchnum": 'random',
                        "gifsearch": list(self.valid_api.keys()),
                        "gifsearchremove": ['gifme'],  # TODO make a config setting
                        "searchlimit": 'default',
                        "nsfw": False,
                        }

        # set defaults if they don't exist
        for key in query_defaults:
            if key not in list(searchdict.keys()):
                searchdict[key] = query_defaults[key]
                if key == "gifsearch":
                    for remx in query_defaults["gifsearchremove"]:
                        searchdict["gifsearch"].remove(remx)

        if botconfig.SpiceBot_Gif.nsfw:
            query_defaults["nsfw"] = True

        # verify query is there to search
        if not searchdict["query"]:
            return {"error": 'No Query to Search'}

        # Replace spaces in search query
        searchdict["searchquery"] = urllib.request.pathname2url(searchdict["query"])

        # set api usage
        if not isinstance(searchdict['gifsearch'], list):
            if str(searchdict['gifsearch']) in list(self.valid_api.keys()):
                searchdict['gifsearch'] = [searchdict['gifsearch']]
            else:
                searchdict['gifsearch'] = list(self.valid_api.keys())
        for apis in searchdict['gifsearch']:
            if apis not in list(self.valid_api.keys()):
                searchdict['gifsearch'].remove(apis)

        # Verify search limit
        if searchdict['searchlimit'] == 'default' or not isinstance(searchdict['searchlimit'], int):
            searchdict['searchlimit'] = 50

        # Random handling for searchnum
        if searchdict["searchnum"] == 'random':
            searchdict["searchnum"] = random.randint(0, searchdict['searchlimit'])

        # verify valid search parameters
        if not str(searchdict["searchnum"]).isdigit():
            return {"error": 'No Search Number or Random Specified'}

        # perform search
        gifapiresults = []
        for currentapi in searchdict['gifsearch']:

            # check if query is already cached
            searchfor = True
            if searchdict["searchquery"].lower() in list(self.valid_api[currentapi]["cache"].keys()):
                if len(self.valid_api[currentapi]["cache"][str(searchdict["searchquery"]).lower()]):
                    searchfor = False
                    verifygoodlinks = []
                    for gifresult in self.valid_api[currentapi]["cache"][str(searchdict["searchquery"])]:
                        if gifresult["returnurl"] not in self.badlinks:
                            verifygoodlinks.append(gifresult)
                    self.valid_api[currentapi]["cache"][str(searchdict["searchquery"])] = verifygoodlinks

            if searchfor:
                self.valid_api[currentapi]["cache"][str(searchdict["searchquery"]).lower()] = []
                # assemble url
                url = self.gif_url_assemble(currentapi, str(searchdict["searchquery"]), str(searchdict["searchlimit"]), searchdict['nsfw'])
                # fetch results
                self.fetch_gif_results(currentapi, str(searchdict["searchquery"]), url)

            if len(self.valid_api[currentapi]["cache"][searchdict["searchquery"].lower()]):
                gifapiresults.extend(self.valid_api[currentapi]["cache"][searchdict["searchquery"].lower()])

        if not len(gifapiresults):
            return {"error": "No Results were found for '" + searchdict["query"] + "' in the " + str(spicemanip.main(searchdict['gifsearch'], 'orlist')) + " api(s)"}

        random.shuffle(gifapiresults)
        random.shuffle(gifapiresults)
        randombad = True
        while randombad:
            gifdict = spicemanip.main(gifapiresults, "random")

            try:
                gifpage = requests.get(gifdict["returnurl"], headers=None)
            except Exception as e:
                gifpage = str(e)
                gifpage = None

            if gifpage and not str(gifpage.status_code).startswith(tuple(["4", "5"])):
                randombad = False
            else:
                self.badlinks.append(str(gifdict["returnurl"]))
                newlist = []
                for tempdict in gifapiresults:
                    if tempdict["returnurl"] != gifdict["returnurl"]:
                        newlist.append(tempdict)
                gifapiresults = newlist

        if not len(gifapiresults):
            return {"error": "No Results were found for '" + searchdict["query"] + "' in the " + str(spicemanip.main(searchdict['gifsearch'], 'orlist')) + " api(s)"}

        # return dict
        gifdict['error'] = None
        return gifdict

    def fetch_gif_results(self, currentapi, searchquery, url):
        try:
            page = requests.get(url, headers=self.header)
        except Exception as e:
            page = e
            page = None
        if page and not str(page.status_code).startswith(tuple(["4", "5"])):
            data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
            results = data[self.valid_api[currentapi]['results']]
            resultsarray = []
            for result in results:
                appendresult = False
                cururl = result[self.valid_api[currentapi]['cururl']]
                slashsplit = str(cururl).split("/")
                fileextension = slashsplit[-1]
                if not fileextension or fileextension == '':
                    appendresult = True
                elif str(fileextension).endswith(".gif"):
                    appendresult = True
                elif "." not in str(fileextension):
                    appendresult = True
                if appendresult:
                    resultsarray.append(cururl)
            # make sure there are results
            if len(resultsarray):
                # Create Temp dict for every result
                tempresultnum = 0
                for tempresult in resultsarray:
                    if tempresult not in self.badlinks:
                        tempresultnum += 1
                        tempdict = {
                                    "returnnum": tempresultnum,
                                    "returnurl": tempresult,
                                    "gifapi": currentapi,
                                    }
                        self.valid_api[currentapi]["cache"][str(searchquery).lower()].append(tempdict)

    def gif_url_assemble(self, currentapi, searchquery, searchlimit, searchnsfw):
        # url base
        url = str(self.valid_api[currentapi]['url'])
        # query
        url += str(self.valid_api[currentapi]['query']) + str(searchquery)
        # limit
        url += str(self.valid_api[currentapi]['limit']) + str(searchlimit)
        # nsfw search?
        if searchnsfw:
            url += str(self.valid_api[currentapi]['nsfw'])
        else:
            url += str(self.valid_api[currentapi]['sfw'])
        # api key
        url += str(self.valid_api[currentapi]['key']) + str(self.valid_api[currentapi]['apikey'])
        return url


gif = BotGif()
