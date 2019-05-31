# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""Setup for SpiceBot"""

import sopel.bot
from sopel import tools

import os

from .Config import config as botconfig
from .Logs import logs

from .Channels import SpiceBot_Channels_MainSection
from .Update import SpiceBot_Update_MainSection
from .osd import SopelWrapperOSD, ToolsOSD, SopelOSD, SpiceBot_OSD


def setup(bot):

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

    logs.log('SpiceBot_Config', "Setting Up Configuration")
    bot.config.core.basename = os.path.basename(bot.config.filename).rsplit('.', 1)[0]
    bot.config.core.logs_stdio = os.path.join(bot.config.core.logdir, 'stdio.log')
    # bot.config.core.logs_stdio = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.stdio.log')
    bot.config.core.logs_exceptions = os.path.join(bot.config.core.logdir, 'exceptions.log')
    # bot.config.core.logs_exceptions = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.exceptions.log')
    bot.config.core.logs_raw = os.path.join(bot.config.core.logdir, 'raw.log')
    # bot.config.core.logs_raw = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.raw.log')

    logs.log('SpiceBot_Channels', "Setting Up Configuration")
    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)

    logs.log('SpiceBot_Update', "Initial Setup processing")
    bot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    botconfig.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
