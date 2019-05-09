# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

from sopel_modules.SpiceBot_SBTools import bot_logging
from sopel_modules.SpiceBot_Events.System import bot_events_startup_register, bot_events_recieved, bot_events_trigger

import os

import spicemanip


def configure(config):
    config.define_section("SpiceBot_Logs", SpiceBot_Logs_MainSection, validate=False)
    config.SpiceBot_Logs.configure_setting('logging_channel', 'SpiceBot_Logs channels')


class SpiceBot_Logs_MainSection(StaticSection):
    logging_channel = ValidatedAttribute('logging_channel', default=False)


def setup(bot):
    bot_logging(bot, 'SpiceBot_Logs', "Starting Setup Procedure")
    bot.config.define_section("SpiceBot_Logs", SpiceBot_Logs_MainSection, validate=False)

    bot_events_startup_register(bot, ['2004'])

    bot_logs_setup_check(bot)

    bot_events_trigger(bot, 2004, "SpiceBot_Logs")


def bot_logs_setup_check(bot):
    if 'SpiceBot_Logs' not in bot.memory:
        bot.memory['SpiceBot_Logs'] = {"logs": {"Sopel_systemd": [], "Sopel_stdio": []}, "queue": []}


def shutdown(bot):
    if "SpiceBot_Logs" in bot.memory:
        del bot.memory["SpiceBot_Logs"]


@sopel.module.event('1003')
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    if bot.config.SpiceBot_Logs.logging_channel:
        channel = bot.config.SpiceBot_Logs.logging_channel
        if channel not in bot.channels.keys():
            bot.write(('JOIN', bot.nick, channel))
            if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                bot.write(('SAJOIN', bot.nick, channel))

        bot_logs_setup_check(bot)

        while True:
            try:
                if len(bot.memory['SpiceBot_Logs']["queue"]):
                    bot.say(str(bot.memory['SpiceBot_Logs']["queue"][0]), channel)
                    del bot.memory['SpiceBot_Logs']["queue"][0]
            except KeyError:
                return


def stdio_logs_fetch(bot):

    logfile = os.path.os.path.join(bot.config.core.logdir, 'stdio.log')

    try:
        log_file_lines = []
        log_file = open(logfile, 'r')
        lines = log_file.readlines()
        for line in lines:
            log_file_lines.append(line)
        log_file.close()

        currentline, linenumindex = 0, []
        for line in log_file_lines:
            if line.startswith("Welcome to Sopel. Loading modules..."):
                linenumindex.append(currentline)
            currentline += 1
        last_start = max(linenumindex)
        debuglines = log_file_lines[last_start:]
    except Exception as e:
        debuglines = e
        debuglines = []

    return debuglines


def systemd_logs_fetch(bot):
    servicepid = get_running_pid(bot)
    debuglines = []
    for line in os.popen(str("sudo journalctl _PID=" + str(servicepid))).read().split('\n'):
        line = str(line).split(str(os.uname()[1] + " "))[-1]
        lineparts = str(line).split(": ")
        del lineparts[0]
        line = spicemanip.main(lineparts, 0)
        if not line.isspace():
            debuglines.append(str(line))
    return debuglines


def get_running_pid(bot):
    try:
        filename = "/run/sopel/" + str(bot.nick) + ".pid"
        with open(filename, 'r') as pid_file:
            pidnum = int(pid_file.read())
    except Exception as e:
        pidnum = e
        pidnum = str(os.popen("systemctl show " + str(bot.nick) + " --property=MainPID").read()).split("=")[-1]
    return pidnum


@sopel.module.event('2004')
@sopel.module.rule('.*')
def bot_events_setup(bot, trigger):
    bot_events_recieved(bot, trigger.event)
