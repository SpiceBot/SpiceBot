# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot OSD system.
"""

from sopel import tools
from sopel.tools import Identifier
from sopel.config.types import StaticSection, ValidatedAttribute

import time
from collections import abc
import sys

from .Server import server as botserver


class SpiceBot_OSD(StaticSection):

    """MAXTARG"""
    notice = ValidatedAttribute('notice', default=1)
    privmsg = ValidatedAttribute('privmsg', default=1)

    flood_burst_lines = ValidatedAttribute('flood_burst_lines', int, default=4)
    """How many messages can be sent in burst mode."""

    flood_empty_wait = ValidatedAttribute('flood_empty_wait', float, default=0.7)
    """How long to wait between sending messages when not in burst mode, in seconds."""

    flood_refill_rate = ValidatedAttribute('flood_refill_rate', int, default=1)
    """How quickly burst mode recovers, in messages per second."""

    flood_throttle = ValidatedAttribute('flood_throttle', bool, default=True)
    """Whether messages will be throttled if too many are sent in a short time."""

    flood_dots = ValidatedAttribute('flood_dots', bool, default=True)
    """Whether repeated messages will be replaced with '...', then dropped."""


class ToolsOSD:

    def get_message_recipientgroups(bot, recipients, text_method):
        """
        Split recipients into groups based on server capabilities.
        This defaults to 4

        Input can be
            * unicode string
            * a comma-seperated unicode string
            * list
            * dict_keys handy for list(bot.channels.keys())
        """

        if sys.version_info.major >= 3:
            if isinstance(recipients, abc.KeysView):
                recipients = [x for x in recipients]
        if isinstance(recipients, dict):
            recipients = [x for x in recipients]

        if not isinstance(recipients, list):
            recipients = recipients.split(",")

        if not len(recipients):
            raise ValueError("Recipients list empty.")

        if text_method == 'NOTICE':
            maxtargets = botserver.isupport["TARGMAX"]["NOTICE"]
        elif text_method in ['PRIVMSG', 'ACTION']:
            maxtargets = botserver.isupport["TARGMAX"]["PRIVMSG"]
        maxtargets = int(maxtargets)

        recipientgroups = []
        while len(recipients):
            recipients_part = ','.join(x for x in recipients[-maxtargets:])
            recipientgroups.append(recipients_part)
            del recipients[-maxtargets:]

        return recipientgroups

    def get_available_message_bytes(bot, recipientgroups, text_method):
        """
        Get total available bytes for sending a message line

        Total sendable bytes is 512
            * 15 are reserved for basic IRC NOTICE/PRIVMSG and a small buffer.
            * The bots hostmask plays a role in this count
                Note: if unavailable, we calculate the maximum length of a hostmask
            * The recipients we send to also is a factor. Multiple recipients reduces
              sendable message length
        """

        if text_method == 'ACTION':
            text_method = 'PRIVMSG'

        # available_bytes = 512
        # reserved_irc_bytes = 15
        # available_bytes -= reserved_irc_bytes
        try:
            hostmaskbytes = len((bot.users.get(bot.nick).hostmask).encode('utf-8'))
        except AttributeError:
            # hostmaskbytes = len((bot.nick).encode('utf-8')) + 12 + 63
            hostmaskbytes = (len((bot.nick).encode('utf-8'))  # Bot's NICKLEN
                             + 1  # (! separator)
                             + len('~')  # (for the optional ~ in user)
                             + 9  # max username length (was 12)
                             + 1  # (@ separator)
                             + 63  # <hostname> has a maximum length of 63 characters.
                             )
        # available_bytes -= hostmaskbytes

        # find the maximum target group length, and use the max
        groupbytes = []
        for recipients_part in recipientgroups:
            groupbytes.append(len((recipients_part).encode('utf-8')))

        max_recipients_bytes = max(groupbytes)
        # available_bytes -= max_recipients_bytes

        allowedLength = (512
                         - len(':') - hostmaskbytes
                         - len(' ' + text_method + ' ')
                         - max_recipients_bytes
                         - len(' :')
                         - len('\r\n')
                         )

        return allowedLength

    def get_sendable_message_list(messages, max_length=400):
        """Get a sendable ``text`` message list.
        :param str txt: unicode string of text to send
        :param int max_length: maximum length of the message to be sendable
        :return: a tuple of two values, the sendable text and its excess text
        We're arbitrarily saying that the max is 400 bytes of text when
        messages will be split. Otherwise, we'd have to account for the bot's
        hostmask, which is hard.
        The `max_length` is the max length of text in **bytes**, but we take
        care of unicode 2-bytes characters, by working on the unicode string,
        then making sure the bytes version is smaller than the max length.
        """

        if not isinstance(messages, list):
            messages = [messages]

        messages_list = ['']
        message_padding = 4 * " "

        for message in messages:
            if len((messages_list[-1] + message_padding + message).encode('utf-8')) <= max_length:
                if messages_list[-1] == '':
                    messages_list[-1] = message
                else:
                    messages_list[-1] = messages_list[-1] + message_padding + message
            else:
                text_list = []
                while len(message.encode('utf-8')) > max_length and not message.isspace():
                    last_space = message.rfind(' ', 0, max_length)
                    if last_space == -1:
                        # No last space, just split where it is possible
                        splitappend = message[:max_length]
                        if not splitappend.isspace():
                            text_list.append(splitappend)
                        message = message[max_length:]
                    else:
                        # Split at the last best space found
                        splitappend = message[:last_space]
                        if not splitappend.isspace():
                            text_list.append(splitappend)
                        message = message[last_space:]
                if len(message.encode('utf-8')) and not message.isspace():
                    text_list.append(message)
                messages_list.extend(text_list)

        return messages_list


class SopelOSD:

    def osd(self, messages, recipients=None, text_method='PRIVMSG', max_messages=-1):
        """Send ``text`` as a PRIVMSG, CTCP ACTION, or NOTICE to ``recipients``.

        In the context of a triggered callable, the ``recipient`` defaults to
        the channel (or nickname, if a private message) from which the message
        was received.

        By default, unless specified in the configuration file, there is some
        built-in flood protection. Messages displayed over 5 times in 2 minutes
        will be displayed as '...'.

        The ``recipient`` can be in list format or a comma seperated string,
        with the ability to send to multiple recipients simultaneously. The
        default recipients that the bot will send to is 4 if the IRC server
        doesn't specify a limit for TARGMAX.

        Text can be sent to this function in either string or list format.
        List format will insert as small buffering space between entries in the
        list.

        There are 512 bytes available in a single IRC message. This includes
        hostmask of the bot as well as around 15 bytes of reserved IRC message
        type. This also includes the destinations/recipients of the message.
        This will split given strings/lists into a displayable format as close
        to the maximum 512 bytes as possible.

        If ``max_messages`` is given, the split mesage will display in as many
        lines specified by this argument. Specifying ``0`` or a negative number
        will display without limitation. By default this is set to ``-1`` when
        called directly. When called from the say/msg/reply/notice/action it
        will default to ``1``.
        """

        if not hasattr(self, 'osdstack'):
            self.osdstack = {}

        text_method = text_method.upper()
        if text_method == 'SAY' or text_method not in ['NOTICE', 'ACTION']:
            text_method = 'PRIVMSG'

        recipientgroups = tools.get_message_recipientgroups(self, recipients, text_method)
        available_bytes = tools.get_available_message_bytes(self, recipientgroups, text_method)
        messages_list = tools.get_sendable_message_list(messages, available_bytes)

        if max_messages >= 1:
            messages_list = messages_list[:max_messages]

        text_method_orig = text_method

        for recipientgroup in recipientgroups:
            text_method = text_method_orig

            recipient_id = Identifier(recipientgroup)

            recipient_stack = self.osdstack.setdefault(recipient_id, {
                'messages': [],
                'flood_left': self.config.SpiceBot_OSD.flood_burst_lines,
                'dots': 0,
            })
            recipient_stack['dots'] = 0

            for text in messages_list:

                try:

                    self.sending.acquire()

                    if recipient_stack['messages']:
                        elapsed = time.time() - recipient_stack['messages'][-1][0]
                    else:
                        # Default to a high enough value that we won't care.
                        # Five minutes should be enough not to matter anywhere below.
                        elapsed = 300

                    if not recipient_stack['flood_left']:
                        recipient_stack['flood_left'] = min(
                            self.config.SpiceBot_OSD.flood_burst_lines,
                            int(elapsed) * self.config.SpiceBot_OSD.flood_refill_rate)

                    if not recipient_stack['flood_left']:
                        penalty = float(max(0, len(text) - 50)) / 70
                        # Never wait more than 2 seconds
                        wait = min(self.config.SpiceBot_OSD.flood_empty_wait + penalty, 2)
                        if elapsed < wait and self.config.SpiceBot_OSD.flood_throttle:
                            time.sleep(wait - elapsed)

                        # Loop detection
                        messages = [m[1] for m in recipient_stack['messages'][-8:]]

                        if self.config.SpiceBot_OSD.flood_dots:
                            # If what we about to send repeated at least 5 times in the
                            # last 2 minutes, replace with '...'
                            if messages.count(text) >= 5 and elapsed < 120:
                                recipient_stack['dots'] += 1
                            else:
                                recipient_stack['dots'] = 0

                    if recipient_stack['dots'] <= 3:

                        recipient_stack['flood_left'] = max(0, recipient_stack['flood_left'] - 1)
                        recipient_stack['messages'].append((time.time(), self.safe(text)))
                        recipient_stack['messages'] = recipient_stack['messages'][-10:]

                        if recipient_stack['dots']:
                            text = '...'
                            if text_method == 'ACTION':
                                text_method = 'PRIVMSG'
                        if text_method == 'ACTION':
                            text = '\001ACTION {}\001'.format(text)
                            self.write(('PRIVMSG', recipientgroup), text)
                            text_method = 'PRIVMSG'
                        elif text_method == 'NOTICE':
                            self.write(('NOTICE', recipientgroup), text)
                        else:
                            self.write(('PRIVMSG', recipientgroup), text)

                finally:
                    self.sending.release()


class SopelWrapperOSD(object):

    def osd(self, messages, recipients=None, text_method='PRIVMSG', max_messages=-1):
        if recipients is None:
            recipients = self._trigger.sender
        self._bot.osd(self, messages, recipients, text_method, max_messages)
