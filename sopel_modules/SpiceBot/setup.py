# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""Setup for SpiceBot"""

from .Logs import logs

from .Channels import SpiceBot_Channels_MainSection


def setup(bot):

    logs.log('SpiceBot_Channels', "Setting Up Configuration")
    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
