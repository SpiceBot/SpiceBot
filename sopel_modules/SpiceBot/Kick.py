# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Update system.
"""

from sopel.config.types import StaticSection, ValidatedAttribute


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
