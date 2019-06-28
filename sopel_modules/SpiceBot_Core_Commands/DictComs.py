# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot DictCom system
"""

# sopel imports
import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip

from word2number import w2n
from random import randint


@SpiceBot.prerun('module', 'dictcom')
@sopel.module.commands('(.*)')
def command_dictcom(bot, trigger, botcom):

    if trigger.sb['com'] not in list(SpiceBot.commands.dict['commands']["dictcom"].keys()):
        return

    bot_dictcom_process(bot, trigger)


def bot_dictcom_process(bot, trigger):

    # use the default key, unless otherwise specified
    trigger.sb["responsekey"] = "?default"

    # handling for special cases
    posscom = spicemanip.main(trigger.sb['args'], 1)
    if posscom.lower() in [command.lower() for command in trigger.sb["dict"].keys()]:
        for command in trigger.sb["dict"].keys():
            if command.lower() == posscom.lower():
                posscom = command
        trigger.sb["responsekey"] = posscom
        trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')
    trigger.sb["dict"][trigger.sb["responsekey"]]["type"] = trigger.sb["dict"][trigger.sb["responsekey"]]["type"]

    trigger.sb["nonstockoptions"] = []
    for command in trigger.sb["dict"].keys():
        if command not in ["?default", "validcoms", "type", "hardcoded_channel_block"]:
            trigger.sb["nonstockoptions"].append(command)

    # This allows users to specify which reply by number by using an ! and a digit (first or last in string)
    validspecifides = ['last', 'random', 'count', 'view', 'add', 'del', 'remove', 'special']
    trigger.sb["specified"] = None
    argone = spicemanip.main(trigger.sb['args'], 1)
    if str(argone).startswith("--") and len(str(argone)) > 2:
        if str(argone[2:]).isdigit():
            trigger.sb["specified"] = int(argone[2:])
        elif SpiceBot.inlist(str(argone[2:]), validspecifides):
            trigger.sb["specified"] = str(argone[2:]).lower()
        elif SpiceBot.inlist(str(argone[2:]), trigger.sb["nonstockoptions"]):
            trigger.sb["specified"] = str(argone[2:]).lower()
            trigger.sb["responsekey"] = trigger.sb["specified"]
        else:
            try:
                trigger.sb["specified"] = w2n.word_to_num(str(argone[1:]))
                trigger.sb["specified"] = int(trigger.sb["specified"])
            except ValueError:
                trigger.sb["specified"] = None
        if trigger.sb["specified"]:
            trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')

    # commands that can be updated
    if trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"]:
        if trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"] == "shared":
            SpiceBot.dictcoms.adjust_nick_array(str(SpiceBot.config.nick), 'sayings', trigger.sb["realcom"] + "_" + str(trigger.sb["responsekey"]), trigger.sb["dict"][trigger.sb["responsekey"]]["responses"], 'startup')
            trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] = SpiceBot.get_nick_value(str(bot.nick), trigger.sb["dict"]["validcoms"][0] + "_" + str(trigger.sb["responsekey"]), 'sayings') or []
        elif trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"] == "user":
            SpiceBot.dictcoms.adjust_nick_array(str(trigger.nick), 'sayings', trigger.sb["realcom"] + "_" + str(trigger.sb["responsekey"]), trigger.sb["dict"][trigger.sb["responsekey"]]["responses"], 'startup')
            trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] = SpiceBot.get_nick_value(str(trigger.nick), trigger.sb["dict"]["validcoms"][0] + "_" + str(trigger.sb["responsekey"]), 'sayings') or []

    if trigger.sb["specified"] == 'special':
        nonstockoptions = spicemanip.main(trigger.sb["nonstockoptions"], "andlist")
        return bot.osd("The special options for " + str(trigger.sb["realcom"]) + " command include: " + str(nonstockoptions) + ".")

    elif trigger.sb["specified"] == 'count':
        return bot.osd("The " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " command has " + str(len(trigger.sb["dict"][trigger.sb["responsekey"]]["responses"])) + " entries.")

    elif trigger.sb["specified"] == 'view':
        if trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] == []:
            return bot.osd("The " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " command appears to have no entries!")
        else:
            bot.osd("The " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " command contains:", trigger.nick, 'notice')
            listnumb, relist = 1, []
            for item in trigger.sb["dict"][trigger.sb["responsekey"]]["responses"]:
                if isinstance(item, dict):
                    relist.append(str("[#" + str(listnumb) + "] COMPLEX dict Entry"))
                elif isinstance(item, list):
                    relist.append(str("[#" + str(listnumb) + "] COMPLEX list Entry"))
                else:
                    relist.append(str("[#" + str(listnumb) + "] " + str(item)))
            bot.osd(relist, trigger.nick)
            return

    elif trigger.sb["specified"] == 'add':

        if not trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"]:
            return bot.osd("The " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list cannot be updated.")

        fulltext = spicemanip.main(trigger.sb['args'], 0)
        if not fulltext:
            return bot.osd("What would you like to add to the " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list?")

        if fulltext in trigger.sb["dict"][trigger.sb["responsekey"]]["responses"]:
            return bot.osd("The following was already in the " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list: '" + str(fulltext) + "'")

        if trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"] == "shared":
            SpiceBot.dictcoms.adjust_nick_array(str(bot.nick), 'sayings', trigger.sb["realcom"] + "_" + str(trigger.sb["responsekey"]), fulltext, trigger.sb["specified"])
        elif trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"] == "user":
            SpiceBot.dictcoms.adjust_nick_array(str(trigger.nick), 'sayings', trigger.sb["realcom"] + "_" + str(trigger.sb["responsekey"]), fulltext, trigger.sb["specified"])

        return bot.osd("The following was added to the " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list: '" + str(fulltext) + "'")

    elif trigger.sb["specified"] in ['del', 'remove']:

        if not trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"]:
            return bot.osd("The " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list cannot be updated.")

        fulltext = spicemanip.main(trigger.sb['args'], 0)
        if not fulltext:
            return bot.osd("What would you like to remove from the " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list?")

        if fulltext not in trigger.sb["dict"][trigger.sb["responsekey"]]["responses"]:
            return bot.osd("The following was already not in the " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list: '" + str(fulltext) + "'")

        if trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"] == "shared":
            SpiceBot.dictcoms.adjust_nick_array(str(bot.nick), 'sayings', trigger.sb["realcom"] + "_" + str(trigger.sb["responsekey"]), fulltext, trigger.sb["specified"])
        elif trigger.sb["dict"][trigger.sb["responsekey"]]["updates_enabled"] == "user":
            SpiceBot.dictcoms.adjust_nick_array(str(trigger.nick), 'sayings', trigger.sb["realcom"] + "_" + str(trigger.sb["responsekey"]), fulltext, trigger.sb["specified"])

        return bot.osd("The following was removed from the " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " entry list: '" + str(fulltext) + "'")

    elif trigger.sb["specified"] and not trigger.sb["dict"][trigger.sb["responsekey"]]["selection_allowed"]:
        return bot.osd("The " + str(trigger.sb["realcom"]) + " " + str(trigger.sb["responsekey"] or '') + " response list cannot be specified.")

    trigger.sb["target"] = False

    trigger.sb["success"] = True
    if trigger.sb["dict"][trigger.sb["responsekey"]]["type"] in ['simple', 'fillintheblank', "target", 'targetplusreason', 'sayings', "readfromfile", "readfromurl", "ascii_art", "translate", "responses"]:
        return bot_dictcom_responses(bot, trigger)
    else:
        command_function_run = str('bot_dictcom_' + trigger.sb["dict"][trigger.sb["responsekey"]]["type"] + '(bot, trigger)')
        eval(command_function_run)


def bot_dictcom_responses(bot, trigger):

    commandrunconsensus = []
    reaction = False

    # A target is required
    if trigger.sb["dict"][trigger.sb["responsekey"]]["target_required"]:

        # try first term as a target
        posstarget = spicemanip.main(trigger.sb['args'], 1) or 0
        targetbypass = trigger.sb["dict"][trigger.sb["responsekey"]]["target_bypass"]
        targetchecking = SpiceBot.users.target_check(bot, trigger, posstarget, targetbypass)
        if not targetchecking["targetgood"]:

            if trigger.sb["dict"][trigger.sb["responsekey"]]["target_backup"]:
                trigger.sb["target"] = trigger.sb["dict"][trigger.sb["responsekey"]]["target_backup"]
                if trigger.sb["target"] == 'instigator':
                    trigger.sb["target"] = trigger.nick
                elif trigger.sb["target"] == 'random':
                    trigger.sb["target"] = SpiceBot.users.random_valid_target(bot, trigger, 'random')
            else:
                for reason in ['self', 'bot', 'bots', 'offline', 'unknown', 'privmsg', 'diffchannel', 'diffbot']:
                    if targetchecking["reason"] == reason and trigger.sb["dict"][trigger.sb["responsekey"]]["react_"+reason]:
                        reaction = True
                        commandrunconsensus.append(trigger.sb["dict"][trigger.sb["responsekey"]]["react_"+reason])
                if not reaction:
                    commandrunconsensus.append([targetchecking["error"]])
        else:
            trigger.sb["target"] = spicemanip.main(trigger.sb['args'], 1)
            trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')

    # $blank input
    trigger.sb["completestring"] = spicemanip.main(trigger.sb['args'], 0) or ''
    if trigger.sb["dict"][trigger.sb["responsekey"]]["blank_required"]:

        if trigger.sb["completestring"] == '' or not trigger.sb["completestring"]:

            if trigger.sb["dict"][trigger.sb["responsekey"]]["blank_backup"]:
                trigger.sb["completestring"] = trigger.sb["dict"][trigger.sb["responsekey"]]["blank_backup"]
            else:
                commandrunconsensus.append(trigger.sb["dict"][trigger.sb["responsekey"]]["blank_fail"])

        if trigger.sb["dict"][trigger.sb["responsekey"]]["blank_phrasehandle"]:
            if trigger.sb["dict"][trigger.sb["responsekey"]]["blank_phrasehandle"] != []:
                if spicemanip.main(trigger.sb["completestring"], 1).lower() not in trigger.sb["dict"][trigger.sb["responsekey"]]["blank_phrasehandle"]:
                    trigger.sb["completestring"] = trigger.sb["dict"][trigger.sb["responsekey"]]["blank_phrasehandle"][0] + " " + trigger.sb["completestring"]
                elif spicemanip.main(trigger.sb["completestring"], 1).lower() in trigger.sb["dict"][trigger.sb["responsekey"]]["blank_phrasehandle"]:
                    if spicemanip.main(trigger.sb["completestring"], 1).lower() != trigger.sb["dict"][trigger.sb["responsekey"]]["blank_phrasehandle"][0]:
                        trigger.sb['args'] = spicemanip.main(trigger.sb['args'], '2+', 'list')
                        if trigger.sb['args'] != []:
                            trigger.sb["completestring"] = trigger.sb["dict"][trigger.sb["responsekey"]]["blank_phrasehandle"][0] + " " + spicemanip.main(trigger.sb['args'], 0)

    if commandrunconsensus != []:
        trigger.sb["success"] = False
        if trigger.sb["dict"][trigger.sb["responsekey"]]["response_fail"] and not reaction:
            trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] = trigger.sb["dict"][trigger.sb["responsekey"]]["response_fail"]
        else:
            trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] = commandrunconsensus[0]

    bot_dictcom_reply_shared(bot, trigger)


def bot_dictcom_reply_shared(bot, trigger):

    if trigger.sb["specified"]:
        if trigger.sb["specified"] > len(trigger.sb["dict"][trigger.sb["responsekey"]]["responses"]):
            currentspecified = len(trigger.sb["dict"][trigger.sb["responsekey"]]["responses"])
        else:
            currentspecified = trigger.sb["specified"]
        trigger.sb["replies"] = spicemanip.main(trigger.sb["dict"][trigger.sb["responsekey"]]["responses"], currentspecified, 'return')
        trigger.sb["replynum"] = currentspecified
    else:
        trigger.sb["replies"] = spicemanip.main(trigger.sb["dict"][trigger.sb["responsekey"]]["responses"], 'random', 'return')
        try:
            trigger.sb["replynum"] = trigger.sb["dict"][trigger.sb["responsekey"]]["responses"].index(trigger.sb["replies"])
        except Exception as e:
            trigger.sb["replynum"] = e
            trigger.sb["replynum"] = 0
        trigger.sb["replynum"] += 1
    trigger.sb["totalreplies"] = len(trigger.sb["dict"][trigger.sb["responsekey"]]["responses"])

    # This handles responses in list form
    if not isinstance(trigger.sb["replies"], list):
        trigger.sb["replies"] = [trigger.sb["replies"]]

    for rply in trigger.sb["replies"]:

        # replies that can be evaluated as code
        if rply.startswith("time.sleep"):
            eval(rply)
        else:

            # random number
            if "$randnum" in rply:
                if trigger.sb["dict"][trigger.sb["responsekey"]]["randnum"]:
                    randno = randint(trigger.sb["dict"][trigger.sb["responsekey"]]["randnum"][0], trigger.sb["dict"][trigger.sb["responsekey"]]["randnum"][1])
                else:
                    randno = randint(0, 50)
                rply = rply.replace("$randnum", str(randno))

            # blank
            if "$blank" in rply:
                rply = rply.replace("$blank", trigger.sb["completestring"] or '')

            # the remaining input
            if "$input" in rply:
                rply = rply.replace("$input", spicemanip.main(trigger.sb['args'], 0) or trigger.sb["realcom"])

            # translation
            if trigger.sb["dict"][trigger.sb["responsekey"]]["translations"]:
                rply = SpiceBot.translate.bot_translate_process(bot, rply, trigger.sb["dict"][trigger.sb["responsekey"]]["translations"])

            # text to precede the output
            if trigger.sb["dict"][trigger.sb["responsekey"]]["prefixtext"] and trigger.sb["success"]:
                rply = spicemanip.main(trigger.sb["dict"][trigger.sb["responsekey"]]["prefixtext"], 'random') + rply

            # text to follow the output
            if trigger.sb["dict"][trigger.sb["responsekey"]]["suffixtext"] and trigger.sb["success"]:
                rply = rply + spicemanip.main(trigger.sb["dict"][trigger.sb["responsekey"]]["suffixtext"], 'random')

            # trigger.nick
            if "$instigator" in rply:
                rply = rply.replace("$instigator", trigger.nick or '')

            # random user
            if "$randuser" in rply:
                if not trigger.is_privmsg:
                    randuser = spicemanip.main(SpiceBot.users.random_valid_target(bot, trigger, 'random'))
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
                targetnames = trigger.sb["target"] or ''
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
                if trigger.sb["dict"][trigger.sb["responsekey"]]["replyvariation"] != []:
                    variation = spicemanip.main(trigger.sb["dict"][trigger.sb["responsekey"]]["replyvariation"], 'random')
                    rply = rply.replace("$replyvariation", variation)
                else:
                    rply = rply.replace("$replyvariation", '')

            # smaller variations for the text
            if "$responsekey" in rply:
                rply = rply.replace("$responsekey", str(trigger.sb["responsekey"]))

            if "$index" in rply:
                rply = rply.replace("$index", str(str(trigger.sb["replynum"]) + "/" + str(trigger.sb["totalreplies"])))

            # display special options for this command
            if "$specialoptions" in rply:
                nonstockoptions = []
                for command in trigger.sb["dict"].keys():
                    if command not in ["?default", "validcoms", "contributors", "author", "type", "filepath", "filename", "hardcoded_channel_block", "description", "exampleresponse", "example", "usage", "privs"]:
                        nonstockoptions.append(command)
                nonstockoptions = spicemanip.main(nonstockoptions, "andlist")
                rply = rply.replace("$specialoptions", nonstockoptions)

            # saying, or action?
            if rply.startswith("*a "):
                rplytype = 'action'
                rply = rply.replace("*a ", "")
            else:
                rplytype = 'say'

            bot.osd(rply, trigger.sender, rplytype)


def bot_dictcom_gif(bot, trigger):

    if trigger.sb["dict"][trigger.sb["responsekey"]]["blank_required"] and not trigger.sb["completestring"]:
        trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] = trigger.sb["dict"][trigger.sb["responsekey"]]["blank_fail"]
        return bot_dictcom_reply_shared(bot, trigger)
    elif trigger.sb["dict"][trigger.sb["responsekey"]]["blank_required"] and trigger.sb["completestring"]:
        queries = [trigger.sb["completestring"]]
    else:
        queries = trigger.sb["dict"][trigger.sb["responsekey"]]["responses"]

    # which api's are we using to search
    if "queryapi" in trigger.sb["dict"].keys():
        searchapis = trigger.sb["dict"][trigger.sb["responsekey"]]["queryapi"]
    else:
        searchapis = bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys()

    if trigger.sb["specified"]:
        if trigger.sb["specified"] > len(queries):
            trigger.sb["specified"] = len(queries)
        query = spicemanip.main(queries, trigger.sb["specified"], 'return')
    else:
        query = spicemanip.main(queries, 'random', 'return')

    searchdict = {"query": query, "gifsearch": searchapis}

    # nsfwenabled = get_database_value(bot, bot.nick, 'channels_nsfw') or []
    # if trigger.sender in nsfwenabled:
    #    searchdict['nsfw'] = True
    # TODO

    gifdict = SpiceBot.gif.get_gif(searchdict)

    if gifdict["error"]:
        trigger.sb["success"] = False
        if trigger.sb["dict"][trigger.sb["responsekey"]]["search_fail"]:
            gifdict["error"] = trigger.sb["dict"][trigger.sb["responsekey"]]["search_fail"]
        trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] = [gifdict["error"]]
    else:
        trigger.sb["dict"][trigger.sb["responsekey"]]["responses"] = [str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))]

    trigger.sb["specified"] = False
    bot_dictcom_reply_shared(bot, trigger)


def bot_dictcom_feeds(bot, trigger):
    return bot.osd("WIP")
    """

    if "feeds" not in bot.memory:
        feed_configs(bot)

    bot_startup_requirements_set(bot, "feeds")

    feed = trigger.sb["dict"][trigger.sb["responsekey"]]["responses"][0]
    if feed not in bot.memory['feeds'].keys():
        return bot.osd(feed + " does not appear to be a valid feed.")

    dispmsg = bot_dictcom_feeds_handler(bot, feed, True)
    if dispmsg == []:
        bot.osd(feed + " appears to have had an unknown error.")
    else:
        bot.osd(dispmsg)

    """


def bot_dictcom_search(bot, trigger):
    bot.say("testing done")
