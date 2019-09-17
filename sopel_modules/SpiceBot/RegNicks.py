# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot regnick system.
"""

from sopel.config.types import StaticSection, ValidatedAttribute


class SpiceBot_RegNicks_MainSection(StaticSection):
    announcenew = ValidatedAttribute('regnick', default=False)
