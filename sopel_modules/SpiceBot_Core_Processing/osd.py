# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot OSD system.
"""
import sopel


import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.RPL_ISUPPORT)
@sopel.module.rule('.*')
def parse_event_005_osd(bot, trigger):
    if trigger.args[-1] != 'are supported by this server':
        return
    parameters = trigger.args[1:-1]
    for param in parameters:
        if '=' in param:
            if param.startswith("TARGMAX"):
                param = str(param).split('=')[1]
                settings = str(param).split(',')
                for setting in settings:
                    settingname = str(setting).split(':')[0]
                    if settingname.upper() in ['NOTICE', 'PRIVMSG']:
                        try:
                            value = str(setting).split(':')[1] or None
                        except IndexError:
                            value = None
                        if value:
                            if settingname.upper() == 'NOTICE':
                                bot.config.SpiceBot_OSD.notice = int(value)
                            elif settingname.upper() == 'PRIVMSG':
                                bot.config.SpiceBot_OSD.privmsg = int(value)
