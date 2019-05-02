#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.tools import stderr
from sopel.config.types import StaticSection, ValidatedAttribute

import sopel_modules.osd

from sopel_modules.SpiceBot_SBTools import service_manip, spicebot_update


class SpiceBot_Update_MainSection(StaticSection):
    gitrepo = ValidatedAttribute('gitrepo', default="https://github.com/SpiceBot/SpiceBot")
    gitbranch = ValidatedAttribute('gitrepo', default="master")


def configure(config):
    config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    config.SpiceBot_Update.configure_setting('gitrepo', 'SpiceBot_Update git repo to install')
    config.SpiceBot_Update.configure_setting('gitbranch', 'SpiceBot_Update git branch to install')


def setup(bot):
    stderr("[SpiceBot_Update] Initial Setup processing...")
    bot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)


@sopel.module.nickname_commands('update')
def nickname_comand_chanstats(bot, trigger):

    if not trigger.admin:
        bot.say("You are not authorized to perform this function.")

    stderr("Recieved Command to update.")
    bot.osd("Received command from " + trigger.nick + " to update from Github and restart. Be Back Soon!", bot.channels.keys())

    spicebot_update(bot)

    service_manip(bot, bot.nick, 'restart')
