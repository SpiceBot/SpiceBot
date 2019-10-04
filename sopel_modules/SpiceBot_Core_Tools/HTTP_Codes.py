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
    query = str(query)

    result = SpiceBot.httpcodes.fetch_result(query)

    message = ["[HTTP code search for " + str(query or "") + "]"]

    if not result["error"] or not query:
        message.extend([result["basic"], result["explanation"]])

    elif query in ["urmom", "yourmom"]:
        message.extend(["Too Many Results", "There are too many pages on the internet regarding your mother."])

    elif query == "42":
        message.extend(["The Hitchhiker's Guide To The Galaxy", "The answer to life, the world, and everything."])

    elif query == "69":
        message.extend(["Oral Fixation", "Round and Round they go, where they stop: nobody knows"])

    bot.osd(message)
