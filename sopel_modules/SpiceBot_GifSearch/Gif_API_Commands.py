# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from .gifsearch import getGif

import sopel.module

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.events.check_ready([SpiceBot.events.BOT_GIFSEARCH])
@SpiceBot.prerun.prerun('prefix')
@sopel.module.commands('(.*)')
def gifapi_triggers(bot, trigger):

    if trigger.sb['com'] not in bot.memory["SpiceBot_GifSearch"]['valid_gif_api_dict'].keys():
        return

    if not len(trigger.sb['args']):
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(trigger.sb['args'], 0)
    searchdict = {"query": query, "gifsearch": trigger.sb['com']}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
