# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.cli import run

from sopel_modules.SpiceBot_Events.System import bot_events_recieved
from sopel_modules.SpiceBot_SBTools import command_permissions_check

import spicemanip

import os


@sopel.module.event('2005')
@sopel.module.rule('.*')
def bot_startup_monologue_start(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    debuglines = errordisplay_fetch(bot)

    # Check for python module errors during this startup
    searchphrasefound = []
    for line in debuglines:
        if "modules failed to load" in str(line) and "0 modules failed to load" not in str(line):
            searchphrase = str(line).replace(" modules failed to load", "")
            searchphrasefound.append(str(searchphrase) + " module(s) failed")
        elif "dict files failed to load" in str(line) and "0 dict files failed to load" not in str(line):
            searchphrase = str(line).replace(" dict files failed to load", "")
            searchphrasefound.append(str(searchphrase) + " dict file(s) failed")

    if len(searchphrasefound):
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        bot.osd(searchphrasefound, bot.channels.keys())


@sopel.module.nickname_commands('debug')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    bot.osd("Is Examining systemd Log(s).", trigger.sender, 'ACTION')

    debuglines = errordisplay_fetch(bot)

    if len(debuglines) == 0:
        bot.osd("had no log(s) for some reason", trigger.sender, 'ACTION')
        return

    for line in debuglines:
        bot.osd(line)


def errordisplay_fetch(bot):
    # servicepid = str(os.popen("systemctl show " + str(bot.nick) + " --property=MainPID").read()).split("=")[-1]
    servicepid = get_running_pid(bot)
    debuglines = []
    for line in os.popen(str("sudo journalctl _PID=" + str(servicepid))).read().split('\n'):
        if not str(line).startswith("-- Logs begin at"):
            line = str(line).split(str(os.uname()[1] + " "))[-1]
            if not str(line).startswith("sudo"):
                lineparts = str(line).split(": ")
                del lineparts[0]
                line = spicemanip.main(lineparts, 0)
                debuglines.append(str(line))
        else:
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
