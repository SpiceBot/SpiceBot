# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Users system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot
from sopel_modules.spicemanip import spicemanip


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('releasenotes')
def nickname_comand_releasenotes(bot, trigger, botcom):
    newnotes = False
    for notefile in list(SpiceBot.releasenotes.notes.keys()):
        if len(SpiceBot.releasenotes.notes[notefile]["new"]):
            bot.osd(["[" + str(notefile) + "]", spicemanip(SpiceBot.releasenotes.notes[notefile]["new"], 'andlist')])
            newnotes = True
    if not newnotes:
        bot.osd("This bot restart contains no new release notes.")
