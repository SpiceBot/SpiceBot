# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""Setup for SpiceBot"""

import sopel.bot
from sopel import tools

import os

from .Config import config as botconfig
from .Logs import logs
from .Events import events as botevents

from .Channels import SpiceBot_Channels_MainSection
from .Commands import SpiceBot_Commands_MainSection
from .Search import SpiceBot_Search_MainSection
from .Update import SpiceBot_Update_MainSection
from .Reddit import SpiceBot_Reddit_MainSection
from .osd import SopelWrapperOSD, ToolsOSD, SopelOSD, SpiceBot_OSD
from .Kick import SopelWrapperKICK, SopelKICK, SpiceBot_Kick
from .Gif import SpiceBot_Gif_MainSection
from .DictComs import SpiceBot_DictComs_MainSection
from .Sherlock import SpiceBot_Sherlock_MainSection
from .AI import SpiceBot_AI_MainSection
from .RegNicks import SpiceBot_RegNicks_MainSection


def setup(bot):

    # basic config settings
    setup_config(bot)

    # Logs
    setup_logs(bot)

    # Commands
    setup_commands(bot)

    # Commands
    setup_search(bot)

    # OSD
    setup_osd(bot)

    # kick
    setup_kick(bot)

    # update
    setup_update(bot)

    # channels
    setup_channels(bot)

    # AI
    setup_ai(bot)

    # startupmonologue
    setup_startupmonologue(bot)

    setup_gif(bot)

    setup_reddit(bot)

    setup_dictcoms(bot)

    setup_sherlock(bot)

    setup_regnicks(bot)


def setup_config(bot):
    logs.log('SpiceBot_Config', "Setting Up Configuration")
    bot.config.core.basename = os.path.basename(bot.config.filename).rsplit('.', 1)[0]
    bot.config.core.prefix_list = str(bot.config.core.prefix).replace("\\", '').split("|")


def setup_logs(bot):
    logs.log('SpiceBot_Logs', "Starting Setup Procedure")
    botevents.startup_add([botevents.BOT_LOGS])
    bot.config.core.logs_stdio = os.path.join(bot.config.core.logdir, 'stdio.log')
    # bot.config.core.logs_stdio = os.path.os.path.join(bot.config.core.logdir, bot.config.core.basename + '.stdio.log')
    bot.config.core.logs_exceptions = os.path.join(bot.config.core.logdir, 'exceptions.log')
    # bot.config.core.logs_exceptions = os.path.os.path.join(bot.config.core.logdir, bot.config.core.basename + '.exceptions.log')
    bot.config.core.logs_raw = os.path.join(bot.config.core.logdir, 'raw.log')
    # bot.config.core.logs_raw = os.path.os.path.join(bot.config.core.logdir, bot.config.core.basename + '.raw.log')
    botevents.trigger(bot, botevents.BOT_LOGS, "SpiceBot_Logs")


def setup_commands(bot):
    logs.log('SpiceBot_Commands', "Setting Up Configuration")
    botevents.startup_add([botevents.BOT_COMMANDS])
    bot.config.define_section("SpiceBot_Commands", SpiceBot_Commands_MainSection, validate=False)
    bot.config.core.query_list = str(bot.config.SpiceBot_Commands.query_prefix).replace("\\", '').split("|")
    bot.config.core.prefix_list.extend(bot.config.SpiceBot_Commands.query_prefix)


def setup_search(bot):
    logs.log('SpiceBot_Search', "Setting Up Configuration")
    bot.config.define_section("SpiceBot_Search", SpiceBot_Search_MainSection, validate=False)


def setup_startupmonologue(bot):
    logs.log('SpiceBot_StartupMonologue', "Initial Setup processing")
    botevents.startup_add([
                        botevents.BOT_STARTUPMONOLOGUE_CONNECTED,
                        botevents.BOT_STARTUPMONOLOGUE_CHANNELS,
                        botevents.BOT_STARTUPMONOLOGUE_COMMANDS,
                        botevents.BOT_STARTUPMONOLOGUE_AI,
                        botevents.BOT_STARTUPMONOLOGUE_VERSION,
                        ])


def setup_channels(bot):
    logs.log('SpiceBot_Channels', "Setting Up Configuration")
    botevents.startup_add([botevents.BOT_CHANNELS])
    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)


def setup_update(bot):
    logs.log('SpiceBot_Update', "Initial Setup processing")
    bot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    botconfig.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)


def setup_ai(bot):
    logs.log('SpiceBot_AI', "Setting Up Configuration")
    bot.config.define_section("SpiceBot_AI", SpiceBot_AI_MainSection, validate=False)
    bot.config.aibrain = os.path.join(bot.config.homedir, bot.config.core.basename + '.aibrain.brn')
    botevents.startup_add([botevents.BOT_AI])


def setup_osd(bot):
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


def setup_kick(bot):
    # Inject KICK
    logs.log('SpiceBot_Kick', "Implanting Kick function into bot")
    bot.kick = SopelKICK.kick
    sopel.bot.SopelWrapper.kick = SopelWrapperKICK.kick

    # verify config settings for server
    logs.log('SpiceBot_Kick', "Checking for config settings")
    bot.config.define_section("SpiceBot_Kick", SpiceBot_Kick, validate=False)
    botconfig.define_section("SpiceBot_Kick", SpiceBot_Kick, validate=False)


def setup_gif(bot):
    bot.config.define_section("SpiceBot_Gif", SpiceBot_Gif_MainSection, validate=False)


def setup_reddit(bot):
    bot.config.define_section("SpiceBot_Reddit", SpiceBot_Reddit_MainSection, validate=False)


def setup_dictcoms(bot):
    bot.config.define_section("SpiceBot_DictComs", SpiceBot_DictComs_MainSection, validate=False)


def setup_sherlock(bot):
    bot.config.define_section("SpiceBot_Sherlock", SpiceBot_Sherlock_MainSection, validate=False)


def setup_regnicks(bot):
    bot.config.define_section("SpiceBot_regnick", SpiceBot_RegNicks_MainSection, validate=False)
    botconfig.define_section("SpiceBot_regnick", SpiceBot_RegNicks_MainSection, validate=False)
