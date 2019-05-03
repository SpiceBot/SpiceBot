# coding=utf8
"""Sopel OSD

Sopel OSD is a "niche" method of displaying text in a Sopel bot
"""

# pylama:ignore=W0611


from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.bot
from sopel import tools, module
from sopel.tools import stderr, Identifier
from sopel.config.types import StaticSection, ValidatedAttribute

import time
from collections import abc
import sys


__author__ = 'Sam Zick'
__email__ = 'sam@deathbybandaid.net'
__version__ = '0.1.2'


def configure(config):
    config.define_section("MAXTARGCONFIG", MAXTARGCONFIG, validate=False)
    config.MAXTARGCONFIG.configure_setting('notice', 'MAXTARG limit for NOTICE')
    config.MAXTARGCONFIG.configure_setting('privmsg', 'MAXTARG limit for PRIVMSG')


def setup(bot):

    # Inject OSD
    stderr("[Sopel-OSD] Implanting OSD function into bot.")
    bot.osd = SopelOSD.osd
    bot.SopelWrapper.osd = SopelOSD.SopelWrapper.osd
    tools.get_available_message_bytes = ToolsOSD.get_available_message_bytes
    tools.get_sendable_message_list = ToolsOSD.get_sendable_message_list
    tools.get_message_recipientgroups = ToolsOSD.get_message_recipientgroups

    # overwrite default bot messaging
    stderr("[Sopel-OSD] Overwrite Default Sopel messaging commands.")
    bot.SopelWrapper.say = SopelOSD.SopelWrapper.say
    bot.SopelWrapper.action = SopelOSD.SopelWrapper.action
    bot.SopelWrapper.notice = SopelOSD.SopelWrapper.notice
    bot.SopelWrapper.reply = SopelOSD.SopelWrapper.reply

    # verify config settings for server
    stderr("[Sopel-OSD] Checking for config settings.")
    bot.config.define_section("MAXTARGCONFIG", MAXTARGCONFIG, validate=False)


# RPL_ISUPPORT = '005'
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
                    if settingname.upper() in ['NOTICE', 'PRIVMSG']:
                        try:
                            value = str(setting).split(':')[1] or None
                        except IndexError:
                            value = None
                        if value:
                            if settingname.upper() == 'NOTICE':
                                bot.config.MAXTARGCONFIG.notice = int(value)
                            elif settingname.upper() == 'PRIVMSG':
                                bot.config.MAXTARGCONFIG.privmsg = int(value)


class MAXTARGCONFIG(StaticSection):
    notice = ValidatedAttribute('notice', default=1)
    privmsg = ValidatedAttribute('privmsg', default=1)


class ToolsOSD:

    def get_message_recipientgroups(bot, recipients, text_method):
        """
        Split recipients into groups based on server capabilities.
        This defaults to 4

        Input can be
            * unicode string
            * a comma-seperated unicode string
            * list
            * dict_keys handy for bot.channels.keys()
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
            maxtargets = bot.config.MAXTARGCONFIG.notice
        elif text_method in ['PRIVMSG', 'ACTION']:
            maxtargets = bot.config.MAXTARGCONFIG.privmsg
        maxtargets = int(maxtargets)

        recipientgroups = []
        while len(recipients):
            recipients_part = ','.join(x for x in recipients[-maxtargets:])
            recipientgroups.append(recipients_part)
            del recipients[-maxtargets:]

        return recipientgroups

    def get_available_message_bytes(bot, recipientgroups):
        """
        Get total available bytes for sending a message line

        Total sendable bytes is 512
            * 15 are reserved for basic IRC NOTICE/PRIVMSG and a small buffer.
            * The bots hostmask plays a role in this count
                Note: if unavailable, we calculate the maximum length of a hostmask
            * The recipients we send to also is a factor. Multiple recipients reduces
              sendable message length
        """

        available_bytes = 512
        reserved_irc_bytes = 15
        available_bytes -= reserved_irc_bytes
        try:
            hostmaskbytes = len((bot.users.get(bot.nick).hostmask).encode('utf-8'))
        except AttributeError:
            hostmaskbytes = len((bot.nick).encode('utf-8')) + 12 + 63
        available_bytes -= hostmaskbytes

        groupbytes = []
        for recipients_part in recipientgroups:
            groupbytes.append(len((recipients_part).encode('utf-8')))

        max_recipients_bytes = max(groupbytes)
        available_bytes -= max_recipients_bytes

        return available_bytes

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
                while len(message.encode('utf-8')) > max_length:
                    last_space = message.rfind(' ', 0, max_length)
                    if last_space == -1:
                        # No last space, just split where it is possible
                        text_list.append(message[:max_length])
                        message = message[max_length:]
                    else:
                        # Split at the last best space found
                        text_list.append(message[:last_space])
                        message = message[last_space:]
                if len(message.encode('utf-8')):
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

        text_method = text_method.upper()
        if text_method == 'SAY' or text_method not in ['NOTICE', 'ACTION']:
            text_method = 'PRIVMSG'

        recipientgroups = tools.get_message_recipientgroups(self, recipients, text_method)
        available_bytes = tools.get_available_message_bytes(self, recipientgroups)
        messages_list = tools.get_sendable_message_list(messages, available_bytes)

        if max_messages >= 1:
            messages_list = messages_list[:max_messages]

        text_method_orig = text_method

        for recipientgroup in recipientgroups:
            text_method = text_method_orig

            # No messages within the last 3 seconds? Go ahead!
            # Otherwise, wait so it's been at least 0.8 seconds + penalty

            recipient_id = Identifier(recipientgroup)

            recipient_stack = self.stack.setdefault(recipient_id, {
                'messages': [],
                'flood_left': 4,
                'dots': 0,
                # TODO
                # 'flood_left': self.config.core.flood_burst_lines,
            })
            recipient_stack['dots'] = 0

            for text in messages_list:

                try:

                    self.sending.acquire()

                    if not recipient_stack['flood_left']:
                        elapsed = time.time() - recipient_stack['messages'][-1][0]
                        # TODO
                        # recipient_stack['flood_left'] = min(
                        #    self.config.core.flood_burst_lines,
                        #    int(elapsed) * self.config.core.flood_refill_rate)
                        recipient_stack['flood_left'] = min(4, int(elapsed) * 1)

                    if not recipient_stack['flood_left']:
                        elapsed = time.time() - recipient_stack['messages'][-1][0]
                        penalty = float(max(0, len(text) - 50)) / 70
                        # Never wait more than 2 seconds
                        # wait = min(self.config.core.flood_empty_wait + penalty, 2) # TODO
                        wait = min(0.7 + penalty, 2)
                        if elapsed < wait:
                            time.sleep(wait - elapsed)

                        # Loop detection
                        messages = [m[1] for m in recipient_stack['messages'][-8:]]

                        # If what we about to send repeated at least 5 times in the
                        # last 2 minutes, replace with '...'
                        if messages.count(text) >= 5 and elapsed < 120:
                            recipient_stack['dots'] += 1
                        else:
                            recipient_stack['dots'] = 0

                    if not recipient_stack['dots'] >= 3:

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

    class SopelWrapper(object):

        def osd(self, messages, recipients=None, text_method='PRIVMSG', max_messages=-1):
            if recipients is None:
                recipients = self._trigger.sender
            self._bot.osd(self, messages, recipients, text_method, max_messages)

        def say(self, message, destination=None, max_messages=1):
            if destination is None:
                destination = self._trigger.sender
            self._bot.osd(self, message, destination, 'PRIVMSG', 1)
            # self._bot.say(message, destination, max_messages)

        def action(self, message, destination=None, max_messages=1):
            if destination is None:
                destination = self._trigger.sender
            self._bot.osd(self, message, destination, 'ACTION', 1)
            # self._bot.action(message, destination, max_messages)

        def notice(self, message, destination=None, max_messages=1):
            if destination is None:
                destination = self._trigger.sender
            self._bot.osd(self, message, destination, 'NOTICE', 1)
            # self._bot.notice(message, destination, max_messages)

        def reply(self, message, destination=None, reply_to=None, notice=False, max_messages=1):
            if destination is None:
                destination = self._trigger.sender
            if reply_to is None:
                reply_to = self._trigger.nick
            message = '%s: %s' % (reply_to, message)
            if notice:
                self._bot.osd(self, message, destination, 'NOTICE', 1)
            else:
                self._bot.osd(self, message, destination, 'PRIVMSG', 1)
            # self._bot.reply(message, destination, reply_to, notice, max_messages)
