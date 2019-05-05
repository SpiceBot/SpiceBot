#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.config.types import StaticSection, ValidatedAttribute

import os
import pip

import spicemanip

from sopel_modules.SpiceBot_SBTools import service_manip, sopel_triggerargs, command_permissions_check, bot_logging, spicebot_reload


class SpiceBot_Update_MainSection(StaticSection):
    gitrepo = ValidatedAttribute('gitrepo', default="https://github.com/SpiceBot/SpiceBot")
    gitbranch = ValidatedAttribute('gitbranch', default="master")


def configure(config):
    config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    config.SpiceBot_Update.configure_setting('gitrepo', 'SpiceBot_Update git repo to install')
    config.SpiceBot_Update.configure_setting('gitbranch', 'SpiceBot_Update git branch to install')


def setup(bot):
    bot_logging(bot, 'SpiceBot_Update', "Initial Setup processing")
    bot.config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)


def shutdown(bot):
    pass


@sopel.module.nickname_commands('update')
def nickname_comand_chanstats(bot, trigger):

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

    bot_logging(bot, 'SpiceBot_Update', "Received command from " + trigger.nick + " to update from Github and restart")
    bot.osd("Received command from " + trigger.nick + " to update from Github and restart. Be Back Soon!", bot.channels.keys())

    if commandused == 'nodeps':
        spicebot_update(bot, "False")
    if commandused == 'deps':
        spicebot_update(bot, "True")

    # service_manip(bot, bot.nick, 'restart', 'SpiceBot_Update')
    spicebot_reload(bot, 'SpiceBot_Update')


def spicebot_update(bot, deps="False"):

    """
    pipcommand = "sudo pip3 install --upgrade"
    if deps == "False":
        pipcommand += " --no-deps"
    pipcommand += " --force-reinstall"
    pipcommand += " git+" + str(bot.config.SpiceBot_Update.gitrepo) + "@" + str(bot.config.SpiceBot_Update.gitbranch)
    """

    pipcommand = ['install']
    pipcommand.append('--upgrade')
    if deps == "False":
        pipcommand.append('--no-deps')
    pipcommand.append('--force-reinstall')
    pipcommand.append("git+" + str(bot.config.SpiceBot_Update.gitrepo) + "@" + str(bot.config.SpiceBot_Update.gitbranch))
    pip.main(pipcommand)

    bot_logging(bot, 'SpiceBot_Update', "Running `" + pipcommand + "`")
    for line in os.popen(pipcommand).read().split('\n'):
        bot_logging(bot, 'SpiceBot_Update', "    " + line)

    # Remove stock modules, if present
    main_sopel_dir = os.path.dirname(os.path.abspath(sopel.__file__))
    modules_dir = os.path.join(main_sopel_dir, 'modules')
    stockdir = os.path.join(modules_dir, "stock")
    if not os.path.exists(stockdir) or not os.path.isdir(stockdir):
        os.system("sudo mkdir " + stockdir)
    for pathname in os.listdir(modules_dir):
        path = os.path.join(modules_dir, pathname)
        if (os.path.isfile(path) and path.endswith('.py') and not path.startswith('_')):
            os.system("sudo mv " + path + " " + stockdir)
