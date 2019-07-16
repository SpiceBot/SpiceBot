# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel

import sopel_modules.SpiceBot as SpiceBot

wait_time = 24 * 60 * 60  # check once per day

message = (
    'A new Sopel version, {}, is available. I am running {}. Please update '
    'me. Full release notes at {}'
)


@sopel.module.interval(wait_time)
def check_updates_sopel_interval(bot):
    SpiceBot.version.check_sopel()

    msg = message.format(
                        SpiceBot.version.sopel["version_online_num"],
                        SpiceBot.version.sopel["version_local_num"],
                        SpiceBot.version.sopel["notes"]
                        )

    if SpiceBot.version.sopel["version_local"] < SpiceBot.version.sopel["version_online"]:
        bot.osd(msg, bot.config.core.owner)
