# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system.
"""
import sopel

import os

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_READY)
@sopel.module.rule('.*')
def bot_events_complete_ai(bot, trigger):

    for braindir in SpiceBot.botai.braindirs:
        for parsefile in os.listdir(braindir):
            SpiceBot.botai.check_file_parse(parsefile)

    if SpiceBot.botai.dict["counts"]:
        SpiceBot.logs.log('SpiceBot_AI', 'Registered %d %s files,' % (SpiceBot.botai.dict["counts"], 'aiml'))
        SpiceBot.logs.log('SpiceBot_AI', '%d %s files failed to load' % (SpiceBot.botai.dict["failcounts"], 'aiml'), True)
    else:
        SpiceBot.logs.log('SpiceBot_AI', "Warning: Couldn't load any %s files" % ('aiml'))
