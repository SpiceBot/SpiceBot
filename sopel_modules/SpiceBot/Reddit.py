# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Reddit system.
"""

import spicemanip


class BotReddit():
    """This Logs all channels known to the server"""
    def __init__(self):
        self.dict = {}

    def prerun(self, trigger):
        trigger_args = spicemanip.main(trigger.args[1], 'create')
        trigger.sb = {
                        "slashcomm": spicemanip.main(trigger_args, 1).lower()[:1],
                        "command": spicemanip.main(trigger_args, 1).lower()[2:],
                        "args": spicemanip.main(trigger_args, "2+", 'list')
                        }
        return trigger


reddit = BotReddit()
