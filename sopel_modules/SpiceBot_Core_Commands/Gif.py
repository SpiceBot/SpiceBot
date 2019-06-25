# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip

# TODO custom gif shortcut commands


@SpiceBot.prerun('module')
@sopel.module.commands('gif')
def gif_trigger(bot, trigger):

    if not len(trigger.sb['args']):
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(trigger.sb['args'], 0)
    searchapis = list(SpiceBot.gif.valid_api.keys())
    searchdict = {"query": query, "gifsearch": searchapis}

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))


@SpiceBot.prerun('module')
@sopel.module.commands('(.*)')
def gifapi_triggers(bot, trigger):

    if trigger.sb['com'] not in list(SpiceBot.gif.valid_api.keys()):
        return

    if not len(trigger.sb['args']):
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(trigger.sb['args'], 0)
    searchdict = {"query": query, "gifsearch": trigger.sb['com']}

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
