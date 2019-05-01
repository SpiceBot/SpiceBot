#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.tools import stderr


def setup(bot):
    stderr("[SpiceBot_DatabaseCache] Setting up Database Cache.")
    bot.memory['SpiceBot_DatabaseCache'] = dict()
