# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_SBTools import sopel_triggerargs
from sopel_modules.SpiceBot_Events.System import bot_events_check, bot_events_recieved


def setup(bot):
    if 'SpiceBot_InvalidCommand' not in bot.memory:
        bot.memory["SpiceBot_InvalidCommand"] = {"valid": []}


def shutdown(bot):
    if "SpiceBot_InvalidCommand" in bot.memory:
        del bot.memory["SpiceBot_InvalidCommand"]


@sopel.module.event('1004')
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    bot_events_recieved(bot, trigger.event)

    for comtype in bot.memory['SpiceBot_CommandsQuery']['commands'].keys():
        bot.memory["SpiceBot_InvalidCommand"]["valid"].extend(bot.memory['SpiceBot_CommandsQuery']['commands'][comtype].keys())


@sopel.module.commands('(.*)')
def InvalidCommand_triggers(bot, trigger):
    return

    while not bot_events_check(bot, ['1004', '2002']):
        pass

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'prefix_command')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if triggercommand.startswith("."):
        return

    if triggercommand not in bot.memory["SpiceBot_InvalidCommand"]["valid"]:
        invalid_display = ["I don't seem to have a command for " + str(triggercommand) + "!"]
        invalid_display.append("If you have a suggestion for this command, you can run .feature ." + str(triggercommand))
        invalid_display.append("ADD DESCRIPTION HERE!")
        bot.osd(invalid_display, trigger.nick, 'notice')
