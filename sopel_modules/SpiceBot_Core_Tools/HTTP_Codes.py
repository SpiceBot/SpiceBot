# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function

# sopel imports
import sopel.module

from sopel_modules.spicemanip import spicemanip

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('module')
@sopel.module.commands('httpcode')
def bot_command_http_codes(bot, trigger, botcom):
    query = spicemanip(botcom.dict["args"], 1) or None
    if not query:
        return bot.osd("You must provide a HTTP status code to look up.")
    message = ["[HTTP code search for " + str(query) + "]"]
    result = SpiceBot.httpcodes.fetch_result(str(query))
    message.extend([result["basic"], result["explanation"]])
    bot.osd(message)
