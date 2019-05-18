# coding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
import sopel.tools
import sopel.config

import os

import spicemanip


class botlogs():
    """This Is a contained source of log information"""
    def __init__(self):
        self.SpiceBot_Logs = {
                                "list": {"Sopel_systemd": [], "Sopel_stdio": []},
                                "queue": []
                                }
        self.sopel_config = {
                                "logging_channel": True
                                }

    def log(self, logtype, logentry, stdio=False):
        logtitle = "[" + logtype + "]"
        logmessage = logtitle + "    " + logentry

        if self.sopel_config["logging_channel"]:
            self.SpiceBot_Logs["queue"].append(logmessage)

        if stdio:
            sopel.tools.stderr(logmessage)

        if logtype not in self.SpiceBot_Logs["list"].keys():
            self.SpiceBot_Logs["list"][logtype] = []
        self.SpiceBot_Logs["list"][logtype].append(logentry)

    def get_logs(self):
        return []

    def stdio_logs_fetch(self, bot):

        stdio_ignore = []
        for logtype in botlogs.SpiceBot_Logs["list"].keys():
            stdio_ignore.append("[" + logtype + "]")

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
            filelines = log_file_lines[last_start:]
        except Exception as e:
            debuglines = e
            filelines = []

        debuglines = []
        loadedmodules = []
        for line in filelines:
            if line.startswith("Loaded:"):
                loadedmodules.append(str(line).split("Loaded:")[-1])
            else:
                if not line.startswith(tuple(stdio_ignore)) and not line.isspace():
                    debuglines.append(str(line))
        loadedmodules = "Loaded: " + spicemanip.main(loadedmodules, 'andlist')
        debuglines.insert(1, loadedmodules)

        return debuglines

    def systemd_logs_fetch(self, bot):
        servicepid = self.get_running_pid(bot)
        debuglines = []
        for line in os.popen(str("sudo journalctl _PID=" + str(servicepid))).read().split('\n'):
            line = str(line).split(str(os.uname()[1] + " "))[-1]
            lineparts = str(line).split(": ")
            del lineparts[0]
            line = spicemanip.main(lineparts, 0)
            if not line.isspace():
                debuglines.append(str(line))
        return debuglines

    def get_running_pid(self, bot):
        try:
            filename = "/run/sopel/sopel-" + str(bot.nick) + ".pid"
            with open(filename, 'r') as pid_file:
                pidnum = int(pid_file.read())
        except Exception as e:
            pidnum = e
            pidnum = str(os.popen("systemctl show " + str(bot.nick) + " --property=MainPID").read()).split("=")[-1]
        return pidnum


botlogs = botlogs.log()


@sopel.module.event('001')
@sopel.module.rule('.*')
def join_log_channel(bot, trigger):

    if bot.config.core.logging_channel:
        channel = bot.config.core.logging_channel
        if channel not in bot.channels.keys():
            bot.write(('JOIN', bot.nick, channel))
            if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                bot.write(('SAJOIN', bot.nick, channel))

        while True:
            if len(botlogs.SpiceBot_Logs["queue"]):
                bot.say(str(botlogs.SpiceBot_Logs["queue"][0]), channel)
                del botlogs.SpiceBot_Logs["queue"][0]
    else:
        botlogs.sopel_config["logging_channel"] = False
        botlogs.SpiceBot_Logs["queue"] = []


def stdio_logs_fetch(bot):

    stdio_ignore = []
    for logtype in bot.memory['SpiceBot_Logs']["logs"].keys():
        stdio_ignore.append("[" + logtype + "]")

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
        filelines = log_file_lines[last_start:]
    except Exception as e:
        debuglines = e
        filelines = []

    debuglines = []
    loadedmodules = []
    for line in filelines:
        if line.startswith("Loaded:"):
            loadedmodules.append(str(line).split("Loaded:")[-1])
        else:
            if not line.startswith(tuple(stdio_ignore)) and not line.isspace():
                debuglines.append(str(line))
    loadedmodules = "Loaded: " + spicemanip.main(loadedmodules, 'andlist')
    debuglines.insert(1, loadedmodules)

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
