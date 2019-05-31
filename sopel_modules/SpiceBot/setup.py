# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""Setup for SpiceBot"""

import os

from .Logs import logs

from .Channels import SpiceBot_Channels_MainSection


def setup(bot):

    logs.log('SpiceBot_Config', "Setting Up Configuration")
    bot.config.core.basename = os.path.basename(bot.config.filename).rsplit('.', 1)[0]
    bot.config.core.logs_stdio = os.path.join(bot.config.core.logdir, 'stdio.log')
    # bot.config.core.logs_stdio = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.stdio.log')
    bot.config.core.logs_exceptions = os.path.join(bot.config.core.logdir, 'exceptions.log')
    # bot.config.core.logs_exceptions = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.exceptions.log')
    bot.config.core.logs_raw = os.path.join(bot.config.core.logdir, 'raw.log')
    # bot.config.core.logs_raw = os.path.os.path.join(bot.config.core.logdir, bot.config.basename + '.raw.log')

    # logs.log('SpiceBot_Logs', "Setting Up Configuration")

    logs.log('SpiceBot_Channels', "Setting Up Configuration")
    bot.config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
