# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module

from .gifsearch import getGif

import sopel_modules.SpiceBot as SpiceBot

import spicemanip


@SpiceBot.events.check_ready([SpiceBot.events.BOT_GIFSEARCH])
@SpiceBot.prerun.prerun('prefix_command')
@module.commands('gif')
def gif_trigger(bot, trigger):

    if not len(trigger.sb['args']):
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(trigger.sb['args'], 0)
    searchapis = bot.memory["SpiceBot_GifSearch"]['valid_gif_api_dict'].keys()
    searchdict = {"query": query, "gifsearch": searchapis}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
