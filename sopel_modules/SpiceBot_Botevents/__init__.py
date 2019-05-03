# coding=utf8
"""Sopel_BotEvents

Sopel BotEvents is a poor mans way to create module load order dependencies
"""
from __future__ import unicode_literals, absolute_import, division, print_function

from .BotEvents import *
from .Connected import *
from .Startup_Complete import *


__author__ = 'Sam Zick'
__email__ = 'sam@deathbybandaid.net'
__version__ = '0.1.1'
