# coding=utf8
"""Sopel_LoadOrder

Sopel LoadOrder is a poor mans way to create module load order dependencies
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel_modules.SpiceBot_SBTools import bot_logging
import threading


def configure(config):
    pass


def setup(bot):
    # TODO add custom pretrigger events
    bot_logging(bot, 'Sopel_LoadOrder', "Starting Module Events Logging")

    threading.Thread(target=setup_thread, args=(bot,)).start()


def shutdown(bot):
    if "Sopel_LoadOrder" in bot.memory:
        del bot.memory["Sopel_LoadOrder"]


def setup_thread(bot):
    if "Sopel_LoadOrder" not in bot.memory:
        bot.memory["Sopel_LoadOrder"] = {"loaded": [], "startup": []}


def list_bot_events(bot, list_type):
    if "Sopel_LoadOrder" not in bot.memory:
        bot.memory["Sopel_LoadOrder"] = {"loaded": [], "startup": []}
    return bot.memory["Sopel_LoadOrder"][list_type]


def check_bot_events(bot, listreq):
    if "Sopel_LoadOrder" not in bot.memory:
        bot.memory["Sopel_LoadOrder"] = {"loaded": [], "startup": []}
    if not isinstance(listreq, list):
        listreq = [str(listreq)]
    for requirement in listreq:
        if requirement not in bot.memory["Sopel_LoadOrder"]["loaded"]:
            return False
    return True


def set_bot_event(bot, addonreq):
    if "Sopel_LoadOrder" not in bot.memory:
        bot.memory["Sopel_LoadOrder"] = {"loaded": [], "startup": []}
    if not isinstance(addonreq, list):
        addonreq = [str(addonreq)]

    bot.memory["Sopel_LoadOrder"]["loaded"].extend(addonreq)


def startup_bot_event(bot, addonreq):
    if "Sopel_LoadOrder" not in bot.memory:
        bot.memory["Sopel_LoadOrder"] = {"loaded": [], "startup": []}
    if not isinstance(addonreq, list):
        addonreq = [str(addonreq)]

    bot.memory["Sopel_LoadOrder"]["startup"].extend(addonreq)


def check_bot_startup(bot):
    if "Sopel_LoadOrder" not in bot.memory:
        bot.memory["Sopel_LoadOrder"] = {"loaded": [], "startup": []}
    for startupitem in bot.memory["Sopel_LoadOrder"]["startup"]:
        if startupitem not in bot.memory["Sopel_LoadOrder"]["loaded"]:
            return False
    return True
