# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""Setup for SpiceBot"""

import sopel.bot
from sopel import tools

import os

from .Config import config as botconfig
from .Logs import logs
from .Events import events

from .Channels import SpiceBot_Channels_MainSection
from .Update import SpiceBot_Update_MainSection
from .osd import SopelWrapperOSD, ToolsOSD, SopelOSD, SpiceBot_OSD
from .Kick import SopelWrapperKICK, SopelKICK, SpiceBot_Kick
from .AI import SpiceBot_AI_MainSection


def setup(bot):

    logs.log('SpiceBot_Logs', "Starting Setup Procedure")
    events.startup_add([events.BOT_LOGS])
    events.trigger(bot, events.BOT_LOGS, "SpiceBot_Logs")

    # Inject OSD
    logs.log('SpiceBot_OSD', "Implanting OSD function into bot")
    bot.osd = SopelOSD.osd
    sopel.bot.SopelWrapper.osd = SopelWrapperOSD.osd
    tools.get_available_message_bytes = ToolsOSD.get_available_message_bytes
    tools.get_sendable_message_list = ToolsOSD.get_sendable_message_list
    tools.get_message_recipientgroups = ToolsOSD.get_message_recipientgroups

    # verify config settings for server
    logs.log('SpiceBot_OSD', "Checking for config settings")
    bot.config.define_section("SpiceBot_OSD", SpiceBot_OSD, validate=False)
    botconfig.define_section("SpiceBot_OSD", SpiceBot_OSD, validate=False)

    # Inject KICK
    logs.log('SpiceBot_Kick', "Implanting Kick function into bot")
    bot.kick = SopelKICK.kick
    sopel.bot.SopelWrapper.kick = SopelWrapperKICK.kick

    # verify config settings for server
    logs.log('SpiceBot_Kick', "Checking for config settings")
    bot.config.define_section("SpiceBot_Kick", SpiceBot_Kick, validate=False)
    botconfig.define_section("SpiceBot_Kick", SpiceBot_Kick, validate=False)

    bot.config.core.prefix_list = str(bot.config.core.prefix).replace("\\", '').split("|")
    bot.config.core.prefix_list.append("?")

    logs.log('SpiceBot_Config', "Setting Up Configuration")
    bot.config.core.basename = os.path.basename(bot.config.filename).rsplit('.', 1)[0]
    bot.config.core.logs_stdio = os.path.join(bot.config.core.logdir, 'stdio.log')
    # bot.config.core.logs_stdio = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.stdio.log')
    bot.config.core.logs_exceptions = os.path.join(bot.config.core.logdir, 'exceptions.log')
    # bot.config.core.logs_exceptions = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.exceptions.log')
    bot.config.core.logs_raw = os.path.join(bot.config.core.logdir, 'raw.log')
    # bot.config.core.logs_raw = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.raw.log')

    bot.config.aibrain = os.path.join(bot.config.homedir, bot.config.basename + '.aibrain.brn')

    logs.log('SpiceBot_Channels', "Setting Up Configuration")
    events.startup_add([events.BOT_CHANNELS])
    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)

    logs.log('SpiceBot_Commands', "Setting Up Configuration")
    events.startup_add([events.BOT_COMMANDS])

    logs.log('SpiceBot_Update', "Initial Setup processing")
    bot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    botconfig.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)

    logs.log('SpiceBot_StartupMonologue', "Initial Setup processing")
    events.startup_add([
                        events.BOT_STARTUPMONOLOGUE_CONNECTED,
                        events.BOT_STARTUPMONOLOGUE_CHANNELS,
                        events.BOT_STARTUPMONOLOGUE_COMMANDS
                        ])

    logs.log('SpiceBot_AI', "Setting Up Configuration")
    bot.config.define_section("SpiceBot_AI", SpiceBot_AI_MainSection, validate=False)
