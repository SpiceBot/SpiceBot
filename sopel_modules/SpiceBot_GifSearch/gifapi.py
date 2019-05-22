# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from .gifsearch import getGif

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.botevents.check_ready([SpiceBot.botevents.BOT_GIFSEARCH])
@sopel.module.commands('(.*)')
def gifapi_triggers(bot, trigger):

    triggerargs, triggercommand = SpiceBot.sopel_triggerargs(bot, trigger, 'prefix_command')

    if triggercommand not in bot.memory["SpiceBot_GifSearch"]['valid_gif_api_dict'].keys():
        return

    if not len(triggerargs):
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(triggerargs, 0)
    searchdict = {"query": query, "gifsearch": triggercommand}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
