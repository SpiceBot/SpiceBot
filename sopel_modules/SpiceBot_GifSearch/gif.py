# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module

from .gifsearch import getGif

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs

import spicemanip


@module.commands('gif')
def gif_trigger(bot, trigger):

    while "SpiceBot_GifSearch" not in bot.memory:
        pass

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger)
    if triggerargs == []:
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(triggerargs, 0)
    searchapis = bot.memory["SpiceBot_GifSearch"]['valid_gif_api_dict'].keys()
    searchdict = {"query": query, "gifsearch": searchapis}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
