# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Users system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot
from sopel_modules.spicemanip import spicemanip


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('todo')
def nickname_comand_users(bot, trigger, botcom):
    todo_task = spicemanip(SpiceBot.commands.todo_list, 'random')
    bot.osd(["Random TODO task for you: {}.".format(todo_task)])
