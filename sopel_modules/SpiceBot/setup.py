# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""Configuration for SpiceBot"""

import sopel.module

from .Logs import logs
from .Events import events
from .Config import config as botconfig

from .configure import SpiceBot_Channels_MainSection


def setup(bot):

    logs.log('SpiceBot_Channels', "Starting setup procedure")
    events.startup_add([events.BOT_CHANNELS])
    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
    botconfig.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
