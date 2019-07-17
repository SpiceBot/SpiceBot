# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Update system.
"""


from sopel.config.types import StaticSection, ValidatedAttribute


class SpiceBot_Update_MainSection(StaticSection):
    gitrepo = ValidatedAttribute('gitrepo', default="https://github.com/SpiceBot/SpiceBot")
    gitbranch = ValidatedAttribute('gitbranch', default="master")
