# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


def setup(bot):
    SpiceBot.logs.log('SpiceBot_StartupMonologue', "Starting setup procedure")

    if 'SpiceBot_StartupMonologue' not in bot.memory:
        bot.memory['SpiceBot_StartupMonologue'] = []
