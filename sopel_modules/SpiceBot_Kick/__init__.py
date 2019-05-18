# coding=utf8
"""Sopel Kick

Sopel Kick is an easy way to kick users from channels
"""

# pylama:ignore=W0611


from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.bot
from sopel import tools, module
from sopel.tools import Identifier
from sopel.config.types import StaticSection, ValidatedAttribute

from sopel_modules.SpiceBot.Logs import botlogs


import time
from collections import abc
import sys


__author__ = 'Sam Zick'
__email__ = 'sam@deathbybandaid.net'
__version__ = '0.1.2'


def configure(config):
    config.define_section("SpiceBot_Kick", SpiceBot_Kick, validate=False)
    config.SpiceBot_Kick.configure_setting('kick', 'MAXTARG limit for KICK')


def setup(bot):

    # Inject KICK
    botlogs.log('SpiceBot_Kick', "Implanting Kick function into bot")
    bot.kick = SopelKICK.kick
    sopel.bot.SopelWrapper.kick = SopelWrapperKICK.kick

    # verify config settings for server
    botlogs.log('SpiceBot_Kick', "Checking for config settings")
    bot.config.define_section("SpiceBot_Kick", SpiceBot_Kick, validate=False)


@module.event('005')
@module.rule('.*')
def parse_event_005(bot, trigger):
    if trigger.args[-1] != 'are supported by this server':
        return
    parameters = trigger.args[1:-1]
    for param in parameters:
        if '=' in param:
            if param.startswith("TARGMAX"):
                param = str(param).split('=')[1]
                settings = str(param).split(',')
                for setting in settings:
                    settingname = str(setting).split(':')[0]
                    if settingname.upper() in ['KICK']:
                        try:
                            value = str(setting).split(':')[1] or None
                        except IndexError:
                            value = None
                        if value:
                            bot.config.SpiceBot_Kick.kick = int(value)


class SpiceBot_Kick(StaticSection):
    kick = ValidatedAttribute('kick', default=1)


class SopelKICK:

    def kick(self, nick, channel, text=None):
        """Send an IRC KICK command.
        Within the context of a triggered callable, ``channel`` will default to the
        channel in which the call was triggered. If triggered from a private message,
        ``channel`` is required (or the call to ``kick()`` will be ignored).
        The bot must be a channel operator in specified channel for this to work.
        .. versionadded:: 7.0
        """
        self.write(['KICK', channel, nick], text)


class SopelWrapperKICK(object):

    def kick(self, nick, channel=None, message=None):
        if channel is None:
            if self._trigger.is_privmsg:
                raise RuntimeError('Error: KICK requires a channel.')
            else:
                channel = self._trigger.sender
        if nick is None:
            raise RuntimeError('Error: KICK requires a nick.')
        self._bot.kick(nick, channel, message)
