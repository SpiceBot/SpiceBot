#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

import spicemanip

from sopel_modules.SpiceBot.Logs import botlogs
from sopel_modules.SpiceBot_SBTools import sopel_triggerargs, command_permissions_check, spicebot_reload, spicebot_update


class SpiceBot_Update_MainSection(StaticSection):
    gitrepo = ValidatedAttribute('gitrepo', default="https://github.com/SpiceBot/SpiceBot")
    gitbranch = ValidatedAttribute('gitbranch', default="master")


def configure(config):
    config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    config.SpiceBot_Update.configure_setting('gitrepo', 'SpiceBot_Update git repo to install')
    config.SpiceBot_Update.configure_setting('gitbranch', 'SpiceBot_Update git branch to install')


def setup(bot):
    botlogs.log('SpiceBot_Update', "Initial Setup processing")
    bot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)


@sopel.module.nickname_commands('update')
def nickname_comand_update(bot, trigger):

    if not command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.say("I was unable to process this Bot Nick command due to privilege issues.")
        return

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'nickname_command')

    if not len(triggerargs):
        commandused = 'nodeps'
    else:
        commandused = spicemanip.main(triggerargs, 1).lower()

    if commandused not in ['deps', 'nodeps']:
        bot.say("Please specify deps or nodeps")
        return

    triggerargs = spicemanip.main(triggerargs, '2+', 'list')

    quitmessage = "Received command from " + trigger.nick + " to update from Github and restart"
    botlogs.log('SpiceBot_Update', quitmessage)
    bot.osd(quitmessage, bot.channels.keys())

    if commandused == 'nodeps':
        spicebot_update(bot, False)
    if commandused == 'deps':
        spicebot_update(bot, True)

    # service_manip(bot, bot.nick, 'restart', 'SpiceBot_Update')
    spicebot_reload(bot, 'SpiceBot_Update', quitmessage)
