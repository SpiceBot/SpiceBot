# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Logs system.

This Class stores logs in an easy to access manner
"""


import sopel
import os
import spicemanip


class BotLogs():
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
            self.dict["queue"].append(logmessage)

        if stdio:
            sopel.tools.stderr(logmessage)

        if logtype not in self.dict["list"].keys():
            self.dict["list"][logtype] = []
        self.dict["list"][logtype].append(logentry)

    def get_logs(self):
        return []

    def stdio_logs_fetch(self, bot):

        stdio_ignore = []
        for logtype in self.dict["list"].keys():
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


logs = BotLogs()
