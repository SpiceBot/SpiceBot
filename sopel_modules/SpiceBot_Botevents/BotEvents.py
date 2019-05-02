# coding=utf8
"""Sopel_BotEvents

Sopel BotEvents is a poor mans way to create module load order dependencies
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.tools import stderr
import threading


def configure(config):
    pass


def setup(bot):
    stderr("[Sopel_BotEvents] Starting Module Events Logging")

    threading.Thread(target=setup_thread, args=(bot,)).start()


def setup_thread(bot):
    if "Sopel_BotEvents" not in bot.memory:
        bot.memory["Sopel_BotEvents"] = {"loaded": [], "startup": []}


def list_bot_events(bot, list_type):
    if "Sopel_BotEvents" not in bot.memory:
        bot.memory["Sopel_BotEvents"] = {"loaded": [], "startup": []}
    return bot.memory["Sopel_BotEvents"][list_type]


def check_bot_events(bot, listreq):
    if "Sopel_BotEvents" not in bot.memory:
        bot.memory["Sopel_BotEvents"] = {"loaded": [], "startup": []}
    if not isinstance(listreq, list):
        listreq = [str(listreq)]
    for requirement in listreq:
        if requirement not in bot.memory["Sopel_BotEvents"]["loaded"]:
            return False
    return True


def set_bot_event(bot, addonreq):
    if "Sopel_BotEvents" not in bot.memory:
        bot.memory["Sopel_BotEvents"] = {"loaded": [], "startup": []}
    if not isinstance(addonreq, list):
        addonreq = [str(addonreq)]

    bot.memory["Sopel_BotEvents"]["loaded"].extend(addonreq)


def startup_bot_event(bot, addonreq):
    if "Sopel_BotEvents" not in bot.memory:
        bot.memory["Sopel_BotEvents"] = {"loaded": [], "startup": []}
    if not isinstance(addonreq, list):
        addonreq = [str(addonreq)]

    bot.memory["Sopel_BotEvents"]["startup"].extend(addonreq)


def check_bot_startup(bot):
    if "Sopel_BotEvents" not in bot.memory:
        bot.memory["Sopel_BotEvents"] = {"loaded": [], "startup": []}
    for startupitem in bot.memory["Sopel_BotEvents"]["startup"]:
        if startupitem not in bot.memory["Sopel_BotEvents"]["loaded"]:
            return False
    return True
