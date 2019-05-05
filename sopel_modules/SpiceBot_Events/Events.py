#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel

from sopel_modules.SpiceBot_SBTools import bot_logging

import time


def configure(config):
    pass


def setup(bot):
    bot_logging(bot, 'SpiceBot_Events', "Starting setup procedure.")
    bot_events_setup_check(bot)
    bot_events_startup_register(bot, ['1001', '1002', '1003', '1004'])
    bot_events_trigger(bot, 1001, "Welcome to the SpiceBot Events System")


def shutdown(bot):
    if "SpiceBot_Events" in bot.memory:
        del bot.memory["SpiceBot_Events"]


@sopel.module.event('1001')
@sopel.module.rule('.*')
def bot_events_start(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    bot_logging(bot, 'SpiceBot_Events', "Ready To Process module setup procedures")
    bot_events_trigger(bot, 1002, "Ready To Process module setup procedures")

    while not bot_events_startup_check(bot):
        pass
    bot_events_trigger(bot, 1004, "All registered modules setup procedures have completed")


@sopel.module.event('1002')
@sopel.module.rule('.*')
def bot_events_ready(bot, trigger):
    bot_events_recieved(bot, trigger.event)


@sopel.module.event('1003')
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):
    bot_events_recieved(bot, trigger.event)


@sopel.module.event('1004')
@sopel.module.rule('.*')
def bot_events_monologue(bot, trigger):
    bot_events_recieved(bot, trigger.event)
    bot.osd('SpiceBot_Events complete', bot.channels.keys())


@sopel.module.event('001')
@sopel.module.rule('.*')
def bot_startup_connection(bot, trigger):

    if bot_events_check(bot, '1004'):
        return

    while not len(bot.channels.keys()) > 0:
        pass
    time.sleep(1)
    bot_events_trigger(bot, 1003, "Bot Connected to IRC")


def bot_events_trigger(bot, number, message):

    bot_events_setup_check(bot)

    bot.memory["SpiceBot_Events"]["triggers"][str(number)] = message

    pretrigger = sopel.trigger.PreTrigger(
        bot.nick,
        ":SpiceBot_Events " + str(number) + " " + str(bot.nick) + " :" + message
    )
    bot.dispatch(pretrigger)


def bot_events_setup_check(bot):
    if "SpiceBot_Events" not in bot.memory:
        bot.memory["SpiceBot_Events"] = {"triggers": {}, "startup": [], "loaded": []}


def bot_events_check(bot, listreq):

    bot_events_setup_check(bot)

    if not isinstance(listreq, list):
        listreq = [str(listreq)]

    for requirement in listreq:
        if requirement not in bot.memory["SpiceBot_Events"]["loaded"]:
            return False

    return True


def bot_events_startup_register(bot, addonreq):

    bot_events_setup_check(bot)

    if not isinstance(addonreq, list):
        addonreq = [str(addonreq)]

    bot.memory["SpiceBot_Events"]["startup"].extend(addonreq)


def bot_events_recieved(bot, number):

    bot_events_setup_check(bot)

    if str(number) not in bot.memory["SpiceBot_Events"]["loaded"]:
        bot.memory["SpiceBot_Events"]["loaded"].append(str(number))


def bot_events_startup_check(bot):

    bot_events_setup_check(bot)

    for startupitem in bot.memory["SpiceBot_Events"]["startup"]:
        if str(startupitem) not in bot.memory["SpiceBot_Events"]["loaded"]:
            return False

    return True
