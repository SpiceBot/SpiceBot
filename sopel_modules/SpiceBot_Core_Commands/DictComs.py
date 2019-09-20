# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot DictCom system
"""

# sopel imports
import sopel.module

import sopel_modules.SpiceBot as SpiceBot

from sopel_modules.spicemanip import spicemanip

from random import randint
import time


@SpiceBot.prerun('module', 'dictcom')
@sopel.module.commands('(.*)')
def command_dictcom(bot, trigger, botcom):

    if botcom.dict['com'] not in list(SpiceBot.commands.dict['commands']["dictcom"].keys()):
        return

    bot_dictcom_process(bot, trigger, botcom)

    #  import hack TODO
    return
    time.time()


def bot_dictcom_process(bot, trigger, botcom):

    botcom.dict["target"] = False

    botcom.dict["success"] = True
    if botcom.dict["dict"][botcom.dict["responsekey"]]["type"] in ['simple', 'fillintheblank', "target", 'targetplusreason', 'sayings', "readfromfile", "readfromurl", "ascii_art", "translate", "responses", "search"]:
        return bot_dictcom_responses(bot, trigger, botcom)
    else:
        command_function_run = str('bot_dictcom_' + botcom.dict["dict"][botcom.dict["responsekey"]]["type"] + '(bot, trigger, botcom)')
        eval(command_function_run)


def bot_dictcom_responses(bot, trigger, botcom):

    commandrunconsensus = []
    reaction = False

    # A target is required
    if botcom.dict["dict"][botcom.dict["responsekey"]]["target_required"]:

        # try first term as a target
        posstarget = spicemanip(botcom.dict['args'], 1) or 0
        targetbypass = botcom.dict["dict"][botcom.dict["responsekey"]]["target_bypass"]
        targetchecking = SpiceBot.users.target_check(bot, trigger, posstarget, targetbypass)
        if not targetchecking["targetgood"]:

            if botcom.dict["dict"][botcom.dict["responsekey"]]["target_backup"]:
                botcom.dict["target"] = botcom.dict["dict"][botcom.dict["responsekey"]]["target_backup"]
                if botcom.dict["target"] == 'instigator':
                    botcom.dict["target"] = trigger.nick
                elif botcom.dict["target"] == 'random':
                    botcom.dict["target"] = SpiceBot.users.random_valid_target(bot, trigger, 'random')
            else:
                for reason in ['self', 'bot', 'bots', 'offline', 'unknown', 'privmsg', 'diffchannel', 'diffbot']:
                    if targetchecking["reason"] == reason and botcom.dict["dict"][botcom.dict["responsekey"]]["react_"+reason]:
                        reaction = True
                        commandrunconsensus.append(botcom.dict["dict"][botcom.dict["responsekey"]]["react_"+reason])
                if not reaction:
                    commandrunconsensus.append([targetchecking["error"]])
        else:
            botcom.dict["target"] = spicemanip(botcom.dict['args'], 1)
            botcom.dict['args'] = spicemanip(botcom.dict['args'], '2+', 'list')

    # $blank input
    botcom.dict["completestring"] = spicemanip(botcom.dict['args'], 0) or ''
    if botcom.dict["dict"][botcom.dict["responsekey"]]["blank_required"]:

        if botcom.dict["completestring"] == '' or not botcom.dict["completestring"]:

            if botcom.dict["dict"][botcom.dict["responsekey"]]["blank_backup"]:
                botcom.dict["completestring"] = botcom.dict["dict"][botcom.dict["responsekey"]]["blank_backup"]
            else:
                commandrunconsensus.append(botcom.dict["dict"][botcom.dict["responsekey"]]["blank_fail"])

        if botcom.dict["dict"][botcom.dict["responsekey"]]["blank_phrasehandle"]:
            if botcom.dict["dict"][botcom.dict["responsekey"]]["blank_phrasehandle"] != []:
                if spicemanip(botcom.dict["completestring"], 1).lower() not in botcom.dict["dict"][botcom.dict["responsekey"]]["blank_phrasehandle"]:
                    botcom.dict["completestring"] = botcom.dict["dict"][botcom.dict["responsekey"]]["blank_phrasehandle"][0] + " " + botcom.dict["completestring"]
                elif spicemanip(botcom.dict["completestring"], 1).lower() in botcom.dict["dict"][botcom.dict["responsekey"]]["blank_phrasehandle"]:
                    if spicemanip(botcom.dict["completestring"], 1).lower() != botcom.dict["dict"][botcom.dict["responsekey"]]["blank_phrasehandle"][0]:
                        botcom.dict['args'] = spicemanip(botcom.dict['args'], '2+', 'list')
                        if botcom.dict['args'] != []:
                            botcom.dict["completestring"] = botcom.dict["dict"][botcom.dict["responsekey"]]["blank_phrasehandle"][0] + " " + spicemanip(botcom.dict['args'], 0)

    if commandrunconsensus != []:
        botcom.dict["success"] = False
        if botcom.dict["dict"][botcom.dict["responsekey"]]["response_fail"] and not reaction:
            botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = botcom.dict["dict"][botcom.dict["responsekey"]]["response_fail"]
        else:
            botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = commandrunconsensus[0]

    bot_dictcom_reply_shared(bot, trigger, botcom)


def bot_dictcom_reply_shared(bot, trigger, botcom):

    if botcom.dict["specified"]:
        if botcom.dict["specified"] > len(botcom.dict["dict"][botcom.dict["responsekey"]]["responses"]):
            currentspecified = len(botcom.dict["dict"][botcom.dict["responsekey"]]["responses"])
        else:
            currentspecified = botcom.dict["specified"]
        botcom.dict["replies"] = spicemanip(botcom.dict["dict"][botcom.dict["responsekey"]]["responses"], currentspecified, 'return')
        botcom.dict["replynum"] = currentspecified
    else:
        botcom.dict["replies"] = spicemanip(botcom.dict["dict"][botcom.dict["responsekey"]]["responses"], 'random', 'return')
        try:
            botcom.dict["replynum"] = botcom.dict["dict"][botcom.dict["responsekey"]]["responses"].index(botcom.dict["replies"])
        except Exception as e:
            botcom.dict["replynum"] = e
            botcom.dict["replynum"] = 0
        botcom.dict["replynum"] += 1
    botcom.dict["totalreplies"] = len(botcom.dict["dict"][botcom.dict["responsekey"]]["responses"])

    # This handles responses in list form
    if not isinstance(botcom.dict["replies"], list):
        botcom.dict["replies"] = [botcom.dict["replies"]]

    for rply in botcom.dict["replies"]:

        # replies that can be evaluated as code
        if rply.startswith("time.sleep"):
            eval(rply)
        else:

            # random number
            if "$randnum" in rply:
                if botcom.dict["dict"][botcom.dict["responsekey"]]["randnum"]:
                    randno = randint(botcom.dict["dict"][botcom.dict["responsekey"]]["randnum"][0], botcom.dict["dict"][botcom.dict["responsekey"]]["randnum"][1])
                else:
                    randno = randint(0, 50)
                rply = rply.replace("$randnum", str(randno))

            # blank
            if "$blank" in rply:
                rply = rply.replace("$blank", botcom.dict["completestring"] or '')

            # the remaining input
            if "$input" in rply:
                rply = rply.replace("$input", spicemanip(botcom.dict['args'], 0) or botcom.dict["realcom"])

            # translation
            if botcom.dict["dict"][botcom.dict["responsekey"]]["translations"]:
                rply = SpiceBot.translate.bot_translate_process(rply, botcom.dict["dict"][botcom.dict["responsekey"]]["translations"])

            # text to precede the output
            if botcom.dict["dict"][botcom.dict["responsekey"]]["prefixtext"] and botcom.dict["success"]:
                rply = spicemanip(botcom.dict["dict"][botcom.dict["responsekey"]]["prefixtext"], 'random') + rply

            # text to follow the output
            if botcom.dict["dict"][botcom.dict["responsekey"]]["suffixtext"] and botcom.dict["success"]:
                rply = rply + spicemanip(botcom.dict["dict"][botcom.dict["responsekey"]]["suffixtext"], 'random')

            # trigger.nick
            if "$instigator" in rply:
                rply = rply.replace("$instigator", trigger.nick or '')

            # random user
            if "$randuser" in rply:
                if not trigger.is_privmsg:
                    randuser = spicemanip(SpiceBot.users.random_valid_target(trigger, 'random'))
                else:
                    randuser = trigger.nick
                rply = rply.replace("$randuser", randuser)

            # current channel
            if "$channel" in rply:
                rply = rply.replace("$channel", trigger.sender or '')

            # bot.nick
            if "$botnick" in rply:
                rply = rply.replace("$botnick", bot.nick or '')

            # target
            if "$target" in rply:
                targetnames = botcom.dict["target"] or ''
                if "$targets" in rply:
                    if targetnames.lower() == "your":
                        targetnames = targetnames
                    elif targetnames.endswith("s"):
                        targetnames = targetnames + "'"
                    else:
                        targetnames = targetnames + "s"
                    rply = rply.replace("$targets", targetnames)
                else:
                    targetnames = targetnames
                    rply = rply.replace("$target", targetnames)

            # smaller variations for the text
            if "$replyvariation" in rply:
                if botcom.dict["dict"][botcom.dict["responsekey"]]["replyvariation"] != []:
                    variation = spicemanip(botcom.dict["dict"][botcom.dict["responsekey"]]["replyvariation"], 'random')
                    rply = rply.replace("$replyvariation", variation)
                else:
                    rply = rply.replace("$replyvariation", '')

            # smaller variations for the text
            if "$responsekey" in rply:
                rply = rply.replace("$responsekey", str(botcom.dict["responsekey"]))

            if "$index" in rply:
                rply = rply.replace("$index", str(str(botcom.dict["replynum"]) + "/" + str(botcom.dict["totalreplies"])))

            # display special options for this command
            if "$specialoptions" in rply:
                nonstockoptions = spicemanip(botcom.dict["dict"]["nonstockoptions"], "andlist")
                rply = rply.replace("$specialoptions", nonstockoptions)

            # saying, or action?
            if rply.startswith("*a "):
                rplytype = 'action'
                rply = rply.replace("*a ", "")
            else:
                rplytype = 'say'

            bot.osd(rply, trigger.sender, rplytype)


def bot_dictcom_gif(bot, trigger, botcom):

    if botcom.dict["dict"][botcom.dict["responsekey"]]["blank_required"] and not botcom.dict["completestring"]:
        botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = botcom.dict["dict"][botcom.dict["responsekey"]]["blank_fail"]
        return bot_dictcom_reply_shared(bot, trigger, botcom)
    elif botcom.dict["dict"][botcom.dict["responsekey"]]["blank_required"] and botcom.dict["completestring"]:
        queries = [botcom.dict["completestring"]]
    else:
        queries = botcom.dict["dict"][botcom.dict["responsekey"]]["responses"]

    # which api's are we using to search
    if "queryapi" in list(botcom.dict["dict"].keys()):
        searchapis = botcom.dict["dict"][botcom.dict["responsekey"]]["queryapi"]
    else:
        searchapis = list(SpiceBot.gif.valid_api.keys())

    if botcom.dict["specified"]:
        if botcom.dict["specified"] > len(queries):
            botcom.dict["specified"] = len(queries)
        query = spicemanip(queries, botcom.dict["specified"], 'return')
    else:
        query = spicemanip(queries, 'random', 'return')

    searchdict = {"query": query, "gifsearch": searchapis}

    # nsfwenabled = get_database_value(bot, bot.nick, 'channels_nsfw') or []
    # if trigger.sender in nsfwenabled:
    #    searchdict['nsfw'] = True
    # TODO

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        botcom.dict["success"] = False
        if botcom.dict["dict"][botcom.dict["responsekey"]]["search_fail"]:
            gifdict["error"] = botcom.dict["dict"][botcom.dict["responsekey"]]["search_fail"]
        botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = [gifdict["error"]]
    else:
        botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = [str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))]

    botcom.dict["specified"] = False
    bot_dictcom_reply_shared(bot, trigger, botcom)


def bot_dictcom_feeds(bot, trigger, botcom):
    return bot.osd("WIP")
    """

    if "feeds" not in bot.memory:
        feed_configs(bot)

    bot_startup_requirements_set(bot, "feeds")

    feed = botcom.dict["dict"][botcom.dict["responsekey"]]["responses"][0]
    if feed not in bot.memory['feeds'].keys():
        return bot.osd(feed + " does not appear to be a valid feed.")

    dispmsg = bot_dictcom_feeds_handler(bot, feed, True)
    if dispmsg == []:
        bot.osd(feed + " appears to have had an unknown error.")
    else:
        bot.osd(dispmsg)

    """


def bot_dictcom_search(bot, trigger, botcom):

    if botcom.dict["dict"][botcom.dict["responsekey"]]["blank_required"] and not botcom.dict["completestring"]:
        botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = botcom.dict["dict"][botcom.dict["responsekey"]]["blank_fail"]
        return bot_dictcom_reply_shared(bot, trigger, botcom)
    elif botcom.dict["dict"][botcom.dict["responsekey"]]["blank_required"] and botcom.dict["completestring"]:
        searchterm = [botcom.dict["completestring"]]
    else:
        searchterm = botcom.dict["dict"][botcom.dict["responsekey"]]["responses"]

    searchreturn = SpiceBot.google.search(searchterm)

    if not searchreturn:
        botcom.dict["success"] = False
        falimessage = 'I cannot find anything about that'
        if botcom.dict["dict"][botcom.dict["responsekey"]]["search_fail"]:
            falimessage = botcom.dict["dict"][botcom.dict["responsekey"]]["search_fail"]
        botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = falimessage
    else:
        botcom.dict["dict"][botcom.dict["responsekey"]]["responses"] = ["[Information search for '" + str(searchterm) + "']", str(searchreturn)]

    botcom.dict["specified"] = False
    bot_dictcom_reply_shared(bot, trigger, botcom)
