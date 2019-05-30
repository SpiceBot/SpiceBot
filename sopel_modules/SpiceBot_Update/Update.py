#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

import spicemanip

import sopel_modules.SpiceBot as SpiceBot


class SpiceBot_Update_MainSection(StaticSection):
    gitrepo = ValidatedAttribute('gitrepo', default="https://github.com/SpiceBot/SpiceBot")
    gitbranch = ValidatedAttribute('gitbranch', default="master")


def configure(config):
    config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    config.SpiceBot_Update.configure_setting('gitrepo', 'SpiceBot_Update git repo to install')
    config.SpiceBot_Update.configure_setting('gitbranch', 'SpiceBot_Update git branch to install')


def setup(bot):
    SpiceBot.logs.log('SpiceBot_Update', "Initial Setup processing")
    bot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    SpiceBot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)


@SpiceBot.prerun.prerun('nickname')
@sopel.module.nickname_commands('update')
def nickname_comand_update(bot, trigger):

    if not SpiceBot.command_permissions_check(bot, trigger, ['admins', 'owner', 'OP', 'ADMIN', 'OWNER']):
        bot.osd("I was unable to process this Bot Nick command due to privilege issues.")
        return

    if not len(trigger.sb['args']):
        commandused = 'nodeps'
    else:
        commandused = spicemanip.main(trigger.sb['args'], 1).lower()

    if commandused not in ['deps', 'nodeps']:
        bot.osd("Please specify deps or nodeps")
        return

    trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')

    quitmessage = "Received command from " + trigger.nick + " to update from Github and restart"
    SpiceBot.logs.log('SpiceBot_Update', quitmessage)
    bot.osd(quitmessage, bot.channels.keys())

    if commandused == 'nodeps':
        SpiceBot.spicebot_update(False)
    if commandused == 'deps':
        SpiceBot.spicebot_update(True)

    # service_manip(bot.nick, 'restart', 'SpiceBot_Update')
    SpiceBot.spicebot_reload(bot, 'SpiceBot_Update', quitmessage)
