# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.tools import stderr
from sopel.config.types import StaticSection, ValidatedAttribute

import sopel_modules.osd

from sopel_modules.SpiceBot_Botevents.BotEvents import set_bot_event

from sopel_modules.SpiceBot_CommandsQuery.CommandsQuery import commandsquery_register

from sopel_modules.SpiceBot_SBTools import read_directory_json_to_dict

import spicemanip

import os
import urllib
import requests
import json
from fake_useragent import UserAgent
import random
import threading

# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


class GifAPIMainSection(StaticSection):
    extra = ValidatedAttribute('extra', default=None)
    nsfw = ValidatedAttribute('nsfw', default=False)


class GifAPISection(StaticSection):
    apikey = ValidatedAttribute('apikey', default=None)


def configure(config):
    moduledir = os.path.dirname(os.path.abspath(__file__))
    api_dir = os.path.join(moduledir, 'gifapi')
    valid_gif_api_dict = read_directory_json_to_dict([api_dir], "Gif API", "[Sopel-GifSearch] ")

    config.define_section("SopelGifSearch", GifAPIMainSection, validate=False)
    config.SopelGifSearch.configure_setting('extra', 'Sopel-GifSearch API Extra directory')
    config.SopelGifSearch.configure_setting('nsfw', 'Sopel-GifSearch API nsfw content')

    for gif_api in valid_gif_api_dict.keys():
        config.define_section(gif_api, GifAPISection, validate=False)
        gif_api_config = eval("config." + gif_api)
        gif_api_config.configure_setting('apikey', 'GIF API Client ID-' + gif_api)


def setup(bot):

    stderr("[Sopel-GifSearch] Starting Setup Procedure")

    threading.Thread(target=setup_thread, args=(bot,)).start()


def setup_thread(bot):

    bot.memory["Sopel-GifSearch"] = {"cache": {}, "badgiflinks": [], 'valid_gif_api_dict': {}}

    dir_to_scan = []

    moduledir = os.path.dirname(os.path.abspath(__file__))
    api_dir = os.path.join(moduledir, 'gifapi')
    dir_to_scan.append(api_dir)

    bot.config.define_section("SopelGifSearch", GifAPIMainSection, validate=False)
    if bot.config.SopelGifSearch.extra:
        dir_to_scan.append(bot.config.SopelGifSearch.extra)

    valid_gif_api_dict = read_directory_json_to_dict(dir_to_scan, "Gif API", "[Sopel-GifSearch] ")

    for gif_api in valid_gif_api_dict.keys():
        bot.config.define_section(gif_api, GifAPISection, validate=False)
        apikey = eval("bot.config." + gif_api + ".apikey")
        if apikey:
            valid_gif_api_dict[gif_api]["apikey"] = apikey
        else:
            valid_gif_api_dict[gif_api]["apikey"] = None
        bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][gif_api] = valid_gif_api_dict[gif_api]

    set_bot_event(bot, "Sopel-GifSearch")

    while 'Sopel-CommandsQuery' not in bot.memory:
        pass

    for prefix_command in bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'].keys():
        commandsquery_register(bot, "prefix_command", prefix_command)

    stderr("[Sopel-CommandsQuery] Found " + str(len(bot.memory['Sopel-CommandsQuery']["prefix_command"].keys())) + " " + "prefix_command" + " commands.")


@sopel.module.commands('gif')
def gif_trigger(bot, trigger):
    triggerargs = sopel_triggerargs(bot, trigger)
    if triggerargs == []:
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(trigger.args[1], 0)
    searchapis = bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'].keys()
    searchdict = {"query": query, "gifsearch": searchapis}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))


def sopel_triggerargs(bot, trigger, command_type='module_command'):
    triggerargs = []

    if len(trigger.args) > 1:
        triggerargs = spicemanip.main(trigger.args[1], 'create')
    triggerargs = spicemanip.main(triggerargs, 'create')

    if command_type in ['module_command']:
        triggerargs = spicemanip.main(triggerargs, '2+', 'list')
    elif command_type in ['nickname_command']:
        triggerargs = spicemanip.main(triggerargs, '3+', 'list')
    elif command_type in ['prefix_command']:
        prefixcommand = spicemanip.main(triggerargs, 1).lower()[1:]
        triggerargs = spicemanip.main(triggerargs, '2+', 'list')
        return triggerargs, prefixcommand

    return triggerargs


def getGif(bot, searchdict):

    # list of defaults
    query_defaults = {
                    "query": None,
                    "searchnum": 'random',
                    "gifsearch": bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'].keys(),
                    "gifsearchremove": ['gifme'],
                    "searchlimit": 'default',
                    "nsfw": False,
                    }

    if bot.config.SopelGifSearch.nsfw:
        query_defaults["nsfw"] = True

    # set defaults if they don't exist
    for key in query_defaults:
        if key not in searchdict.keys():
            searchdict[key] = query_defaults[key]
            if key == "gifsearch":
                for remx in query_defaults["gifsearchremove"]:
                    searchdict["gifsearch"].remove(remx)

    # Replace spaces in search query
    if not searchdict["query"]:
        return {"error": 'No Query to Search'}
    # searchdict["searchquery"] = searchdict["query"].replace(' ', '%20')
    searchdict["searchquery"] = urllib.request.pathname2url(searchdict["query"])

    # set api usage
    if not isinstance(searchdict['gifsearch'], list):
        if str(searchdict['gifsearch']) in bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'].keys():
            searchdict['gifsearch'] = [searchdict['gifsearch']]
        else:
            searchdict['gifsearch'] = bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'].keys()
    else:
        for apis in searchdict['gifsearch']:
            if apis not in bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'].keys():
                searchdict['gifsearch'].remove(apis)

    # Verify search limit
    if searchdict['searchlimit'] == 'default' or not isinstance(searchdict['searchlimit'], int):
        searchdict['searchlimit'] = 50

    # Random handling for searchnum
    if searchdict["searchnum"] == 'random':
        searchdict["searchnum"] = random.randint(0, searchdict['searchlimit'])

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        return {"error": 'No Query to Search'}

    if not str(searchdict["searchnum"]).isdigit():
        return {"error": 'No Search Number or Random Specified'}

    gifapiresults = []
    for currentapi in searchdict['gifsearch']:

        # url base
        url = str(bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['url'])
        # query
        url += str(bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['query']) + str(searchdict["searchquery"])
        # limit
        url += str(bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['limit']) + str(searchdict["searchlimit"])
        # nsfw search?
        if searchdict['nsfw']:
            url += str(bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['nsfw'])
        else:
            url += str(bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['sfw'])
        # api key
        url += str(bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['key']) + str(bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['apikey'])

        if currentapi not in bot.memory["Sopel-GifSearch"]['cache'].keys():
            bot.memory["Sopel-GifSearch"]['cache'][currentapi] = dict()

        if str(searchdict["searchquery"]) not in bot.memory["Sopel-GifSearch"]['cache'][currentapi].keys():
            bot.memory["Sopel-GifSearch"]['cache'][currentapi][str(searchdict["searchquery"])] = []

        if bot.memory["Sopel-GifSearch"]['cache'][currentapi][str(searchdict["searchquery"])] == []:

            try:
                page = requests.get(url, headers=header)
            except Exception as e:
                page = None

            if page and not str(page.status_code).startswith(tuple(["4", "5"])):

                data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

                results = data[bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['results']]
                resultsarray = []
                for result in results:
                    appendresult = False
                    cururl = result[bot.memory["Sopel-GifSearch"]['valid_gif_api_dict'][currentapi]['cururl']]
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
                if resultsarray != []:

                    # Create Temp dict for every result
                    tempresultnum = 0
                    for tempresult in resultsarray:
                        if tempresult not in bot.memory["Sopel-GifSearch"]["badgiflinks"]:
                            tempresultnum += 1
                            tempdict = dict()
                            tempdict["returnnum"] = tempresultnum
                            tempdict["returnurl"] = tempresult
                            tempdict["gifapi"] = currentapi
                            bot.memory["Sopel-GifSearch"]['cache'][currentapi][str(searchdict["searchquery"])].append(tempdict)

        else:
            verifygoodlinks = []
            for gifresult in bot.memory["Sopel-GifSearch"]['cache'][currentapi][str(searchdict["searchquery"])]:
                if gifresult["returnurl"] not in bot.memory["Sopel-GifSearch"]["badgiflinks"]:
                    verifygoodlinks.append(gifresult)
            bot.memory["Sopel-GifSearch"]['cache'][currentapi][str(searchdict["searchquery"])] = verifygoodlinks

        if bot.memory["Sopel-GifSearch"]['cache'][currentapi][str(searchdict["searchquery"])] != []:
            gifapiresults.extend(bot.memory["Sopel-GifSearch"]['cache'][currentapi][str(searchdict["searchquery"])])

    if gifapiresults == []:
        return {"error": "No Results were found for '" + searchdict["query"] + "' in the " + str(spicemanip.main(searchdict['gifsearch'], 'orlist')) + " api(s)"}

    random.shuffle(gifapiresults)
    random.shuffle(gifapiresults)
    randombad = True
    while randombad:
        gifdict = spicemanip.main(gifapiresults, "random")

        try:
            gifpage = requests.get(gifdict["returnurl"], headers=None)
        except Exception as e:
            gifpage = None

        if gifpage and not str(gifpage.status_code).startswith(tuple(["4", "5"])):
            randombad = False
        else:
            bot.memory["Sopel-GifSearch"]["badgiflinks"].append(gifdict["returnurl"])
            newlist = []
            for tempdict in gifapiresults:
                if tempdict["returnurl"] != gifdict["returnurl"]:
                    newlist.append(tempdict)
            gifapiresults = newlist

    if gifapiresults == []:
        return {"error": "No Results were found for '" + searchdict["query"] + "' in the " + str(spicemanip.main(searchdict['gifsearch'], 'orlist')) + " api(s)"}

    # return dict
    gifdict['error'] = None
    return gifdict
