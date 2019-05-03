# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from .gifsearch import getGif

import sopel.module

import sopel_modules.osd

import spicemanip

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs


@sopel.module.commands('(.*)')
def gifapi_triggers(bot, trigger):

    while "SpiceBot_GifSearch" not in bot.memory:
        pass

    triggerargs, prefixcommand = sopel_triggerargs(bot, trigger, 'prefix_command')

    if prefixcommand not in bot.memory["SpiceBot_GifSearch"]['valid_gif_api_dict'].keys():
        return

    if triggerargs == []:
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(triggerargs, 0)
    searchdict = {"query": query, "gifsearch": prefixcommand}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
