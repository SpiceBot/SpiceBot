# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip

# TODO custom gif shortcut commands


@SpiceBot.prerun('module')
@sopel.module.commands('gif')
def gif_trigger(bot, trigger, botcom):

    if not len(botcom.dict['args']):
        return SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Please present a query to search.")

    query = spicemanip.main(botcom.dict['args'], 0)
    searchapis = list(SpiceBot.gif.valid_api.keys())
    searchdict = {"query": query, "gifsearch": searchapis}

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))


@SpiceBot.prerun('module', "gif_prefix")
@sopel.module.commands('(.*)')
def gifapi_triggers(bot, trigger, botcom):

    if botcom.dict['com'] not in list(SpiceBot.gif.valid_api.keys()):
        return

    if not len(botcom.dict['args']):
        return SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], "Please present a query to search.")

    query = spicemanip.main(botcom.dict['args'], 0)
    searchdict = {"query": query, "gifsearch": botcom.dict['com']}

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        SpiceBot.messagelog.messagelog_error(botcom.dict["log_id"], gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
