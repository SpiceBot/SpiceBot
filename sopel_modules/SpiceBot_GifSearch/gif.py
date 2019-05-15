# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module

from .gifsearch import getGif

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs
from sopel_modules.SpiceBot_Events.System import bot_events_check, botevents

import spicemanip


@module.commands('gif')
def gif_trigger(bot, trigger):

    while not bot_events_check(bot, botevents.BOT_GIFSEARCH):
        pass

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger)
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
