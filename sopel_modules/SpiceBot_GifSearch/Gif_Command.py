# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module

from .gifsearch import getGif

import sopel_modules.SpiceBot as SpiceBot

import spicemanip


@SpiceBot.events.check_ready([SpiceBot.events.BOT_GIFSEARCH])
@module.commands('gif')
def gif_trigger(bot, trigger):

    triggerargs, triggercommand = SpiceBot.sopel_triggerargs(bot, trigger)
    if not len(triggerargs):
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(triggerargs, 0)
    searchapis = bot.memory["SpiceBot_GifSearch"]['valid_gif_api_dict'].keys()
    searchdict = {"query": query, "gifsearch": searchapis}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
