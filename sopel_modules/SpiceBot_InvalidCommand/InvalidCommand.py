# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


def setup(bot):
    if 'SpiceBot_InvalidCommand' not in bot.memory:
        bot.memory["SpiceBot_InvalidCommand"] = {"valid": []}


def shutdown(bot):
    if "SpiceBot_InvalidCommand" in bot.memory:
        del bot.memory["SpiceBot_InvalidCommand"]


@sopel.module.event(SpiceBot.events.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    for comtype in SpiceBot.commands.dict['commands'].keys():
        bot.memory["SpiceBot_InvalidCommand"]["valid"].extend(SpiceBot.commands.dict['commands'][comtype].keys())


@SpiceBot.events.check_ready([SpiceBot.events.BOT_LOADED, SpiceBot.events.BOT_COMMANDSQUERY])
@sopel.module.commands('(.*)')
def InvalidCommand_triggers(bot, trigger):
    return

    triggerargs, triggercommand = SpiceBot.sopel_triggerargs(bot, trigger, 'prefix_command')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if triggercommand.startswith("."):
        return

    if triggercommand not in bot.memory["SpiceBot_InvalidCommand"]["valid"]:
        invalid_display = ["I don't seem to have a command for " + str(triggercommand) + "!"]
        invalid_display.append("If you have a suggestion for this command, you can run .feature ." + str(triggercommand))
        invalid_display.append("ADD DESCRIPTION HERE!")
        bot.osd(invalid_display, trigger.nick, 'notice')
