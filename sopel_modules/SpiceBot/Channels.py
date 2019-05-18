# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Logs system.

This Class stores logs in an easy to access manner
"""


class BotChannels():
    """This Logs all channels known to the server"""
    def __init__(self):
        self.SpiceBot_Channels = {
                                "list": {}
                                }


botchannels = BotChannels()
