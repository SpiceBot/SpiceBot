# coding=utf8
"""Sopel_BotEvents

Sopel BotEvents is a poor mans way to create module load order dependencies
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel_modules.SpiceBot_SBTools import bot_logging
import threading


def configure(config):
    pass


def setup(bot):
    # TODO add custom pretrigger events
    bot_logging(bot, 'Sopel_BotEvents', "Starting Module Events Logging")

    threading.Thread(target=setup_thread, args=(bot,)).start()


def shutdown(bot):
    if "Sopel_BotEvents" in bot.memory:
        del bot.memory["Sopel_BotEvents"]


def setup_thread(bot):
    if "Sopel_BotEvents" not in bot.memory:
        bot.memory["Sopel_BotEvents"] = {"loaded": [], "startup": []}


@sopel.module.event('7777')
@sopel.module.rule('.*')
def parse_event_spicebotdbb(bot, trigger):
    sopel.tools.stderr("\n" + trigger.event + "    " + str(trigger.args) + "\n")


@sopel.module.event('001')
@sopel.module.rule('.*')
def bot_trigger_create(bot, trigger):
    pretrigger = sopel.trigger.PreTrigger(
        bot.nick,
        ":" + bot.nick + " 7777 " + bot.nick +
        " :This is a test of the Fake Event System"
    )
    bot.dispatch(pretrigger)


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
