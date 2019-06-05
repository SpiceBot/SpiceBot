# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""Configuration for SpiceBot"""

from .Channels import SpiceBot_Channels_MainSection
from .AI import SpiceBot_AI_MainSection
from .Update import SpiceBot_Update_MainSection
from .Kick import SpiceBot_Kick
from .osd import SpiceBot_OSD


def configure(config):

    config.define_section("SpiceBot_OSD", SpiceBot_OSD, validate=False)
    config.SpiceBot_OSD.configure_setting('notice', 'MAXTARG limit for NOTICE')
    config.SpiceBot_OSD.configure_setting('privmsg', 'MAXTARG limit for PRIVMSG')
    config.SpiceBot_OSD.configure_setting('flood_burst_lines', 'How many messages can be sent in burst mode.')
    config.SpiceBot_OSD.configure_setting('flood_empty_wait', 'How long to wait between sending messages when not in burst mode, in seconds.')
    config.SpiceBot_OSD.configure_setting('flood_refill_rate', 'How quickly burst mode recovers, in messages per second.')
    config.SpiceBot_OSD.configure_setting('flood_throttle', 'Whether messages will be throttled if too many are sent in a short time.')
    config.SpiceBot_OSD.configure_setting('flood_dots', "Whether repeated messages will be replaced with '...', then dropped.")

    config.define_section("SpiceBot_Channels", SpiceBot_Channels_MainSection, validate=False)
    config.SpiceBot_Channels.configure_setting('announcenew', 'SpiceBot_Channels Announce New Channels')
    config.SpiceBot_Channels.configure_setting('joinall', 'SpiceBot_Channels JOIN New Channels')
    config.SpiceBot_Channels.configure_setting('operadmin', 'SpiceBot_Channels OPER ADMIN MODE')
    config.SpiceBot_Channels.configure_setting('chanignore', 'SpiceBot_Channels Ignore JOIN for channels')

    config.define_section("SpiceBot_Update", SpiceBot_Update_MainSection, validate=False)
    config.SpiceBot_Update.configure_setting('gitrepo', 'SpiceBot_Update git repo to install')
    config.SpiceBot_Update.configure_setting('gitbranch', 'SpiceBot_Update git branch to install')

    config.define_section("SpiceBot_Kick", SpiceBot_Kick, validate=False)
    config.SpiceBot_Kick.configure_setting('kick', 'MAXTARG limit for KICK')

    config.define_section("SpiceBot_AI", SpiceBot_AI_MainSection, validate=False)
    config.SpiceBot_AI.configure_setting('extra', 'extra aiml directories to import matches from')
    config.SpiceBot_AI.configure_setting('gender', 'bot gender')
