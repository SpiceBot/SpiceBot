# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system. Based On Chatty cathy
"""

from sopel.tools import Identifier
from sopel.config.types import StaticSection, ListAttribute, ValidatedAttribute

import os
import tempfile
import aiml

from .Database import db as botdb
from .Config import config as botconfig
from .Read import read as botread
from .Users import users as botusers

from sopel_modules.spicemanip import spicemanip


class SpiceBot_AI_MainSection(StaticSection):
    extra = ListAttribute('extra')
    gender = ValidatedAttribute('gender', default='female')


class SpiceBot_AI():

    def __init__(self):
        self.setup_ai()
        self.braindirs = []
        self.dict = {
                    "patterncounts": 0,
                    "filecounts": 0,
                    "sessioncache": {},
                    "files": {}
                    }
        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()

        # aiml parser
        self.aiml_parser = aiml.AimlParser.create_parser()

        # Don't warn for no matches
        self.aiml_kernel._verboseMode = False

        # Learn responses
        self.load_saved_brain()
        self.load_brain()

        # Load bot values
        self.load_bot_values()

    def setup_ai(self):
        botconfig.define_section("SpiceBot_AI", SpiceBot_AI_MainSection, validate=False)
        botconfig.config.aibrain = os.path.join(botconfig.homedir, botconfig.config.core.basename + '.aibrain.brn')

    def load_saved_brain(self):
        if os.path.isfile(botconfig.config.aibrain):
            self.aiml_kernel.bootstrap(brainFile=botconfig.config.aibrain)
            self.save_brain()

    def load_brain(self):
        braindirs = botread.get_config_dirs("SpiceBot_AI")

        # learn directories
        self.learn(braindirs)
        self.save_brain()

    def load_bot_values(self):

        current_bot_db = botdb.get_plugin_value('SpiceBot_AI', 'brain') or None
        if current_bot_db:
            for predicate in list(current_bot_db.keys()):
                predval = current_bot_db[predicate]
                self.aiml_kernel.setBotPredicate(predicate, predval)

        # sopel nick
        self.aiml_kernel.setBotPredicate("nick", botconfig.nick)

        # gender
        self.aiml_kernel.setBotPredicate("gender", botconfig.SpiceBot_AI.gender.lower())
        if botconfig.SpiceBot_AI.gender.lower() not in ["male", "female"]:
            self.aiml_kernel.setBotPredicate("gendertype", "item")
        else:
            self.aiml_kernel.setBotPredicate("gendertype", botconfig.SpiceBot_AI.gender.lower())

    def learn(self, braindirs):
        for braindir in braindirs:
            if braindir not in self.braindirs:
                self.braindirs.append(braindir)

                # Count matches
                for pathname in os.listdir(braindir):
                    self.dict["filecounts"] += 1
                    aimlfile = os.path.join(braindir, pathname)
                    data = open(aimlfile).read()
                    count = data.count('pattern')
                    count = count / 2
                    self.dict["patterncounts"] += int(count)

                tempbrain = tempfile.mkstemp()[1]
                with open(tempbrain, 'w') as fileo:
                    fileo.write(
                        "<aiml version='1.0.1' encoding='UTF-8'>"
                        "    <!-- std-startup.xml -->\n"
                        "    <category>\n"
                        "        <pattern>LOAD AIML B</pattern>\n"
                        "        <template>\n"
                        "            <learn>{}</learn>\n"
                        "        </template>\n"
                        "    </category>\n"
                        "</aiml>".format(os.path.join(braindir, "*.aiml"))
                    )
                self.aiml_kernel.learn(tempbrain)
        self.aiml_kernel.respond("LOAD AIML B")

    def on_message(self, bot, trigger, message):
        nick = Identifier(trigger.nick)
        nick_id = botusers.get_nick_id(nick, True)
        self.check_user_import(nick, nick_id)

        message = self.bot_message_precipher(bot, trigger, message)
        aiml_response = self.aiml_kernel.respond(message, nick_id)
        if aiml_response:
            aiml_response = self.bot_message_decipher(bot, trigger, aiml_response)

        self.save_nick_session(nick, nick_id)
        self.save_brain()

        return aiml_response

    def bot_message_precipher(self, bot, trigger, message):

        # punctuation
        puct_dict = {"!": "exclamationmark", ".": "period", "?": "questionmark", ",": "comma"}
        for puctuation in list(puct_dict.keys()):
            message = message.replace(puctuation, puct_dict[puctuation])

        # bot items
        for botitem in ["nick"]:
            messagelist = spicemanip(message, "create")
            for i in range(len(messagelist)):
                if messagelist[i].upper() == str(eval("bot." + botitem)).upper():
                    messagelist[i] = str("bot" + botitem).upper()
            message = spicemanip(messagelist, 0)

        for triggeritem in ["nick", "sender"]:
            messagelist = spicemanip(message, "create")
            for i in range(len(messagelist)):
                if messagelist[i].upper() == str(eval("trigger." + botitem)).upper():
                    messagelist[i] = str("trigger" + botitem).upper()
            message = spicemanip(messagelist, 0)

        return message

    def bot_message_decipher(self, bot, trigger, aiml_response):

        # bot items
        for botitem in ["nick"]:
            aiml_response = aiml_response.replace("bot" + botitem, str(eval("bot." + botitem)))

        # trigger items
        for triggeritem in ["nick", "sender"]:
            aiml_response = aiml_response.replace("trigger" + triggeritem, str(eval("trigger." + triggeritem)))

        # pronouns
        botgendertype = self.aiml_kernel.getBotPredicate("gendertype")
        pronounsdict = {
                        "male": {
                                "main": "he",
                                "possess": "his",
                                "self": "himself",
                                },
                        "female": {
                                "main": "her",
                                "possess": "hers",
                                "self": "herself",
                                },
                        "item": {
                                "main": "it",
                                "possess": "its",
                                "self": "itself",
                                },
                        "point": {
                                "main": "you",
                                "possess": "yours",
                                "self": "yourself",
                                },
                        "group": {
                                "main": "them",
                                "possess": "theirs",
                                "self": "themselves",
                                },
                        }
        for pronounitem in list(pronounsdict[botgendertype].keys()):
            aiml_response = aiml_response.replace("BOTPRONOUN" + pronounitem, pronounsdict[botgendertype][pronounitem])
        triggergendertype = self.getPredicate("gender", trigger.nick)
        if not triggergendertype or triggergendertype == "":
            triggergendertype = "point"
        for pronounitem in list(pronounsdict[triggergendertype].keys()):
            aiml_response = aiml_response.replace("TRIGGERPRONOUN" + pronounitem, pronounsdict[triggergendertype][pronounitem])

        aiml_response = "\x0315" + aiml_response + "\x03"

        return aiml_response

    def getPredicate(self, predicate, nick, nick_id=None):
        if not nick_id:
            nick = Identifier(nick)
            nick_id = botusers.get_nick_id(nick, True)
        self.aiml_kernel.getPredicate(predicate, nick_id)

    def check_user_import(self, nick, nick_id=None):
        if not nick_id:
            nick = Identifier(nick)
            nick_id = botusers.get_nick_id(nick, True)
        if nick_id not in list(self.dict["sessioncache"].keys()):
            self.dict["sessioncache"][nick_id] = botdb.get_nick_value(nick, 'botai') or {}
            for predicate in list(self.dict["sessioncache"][nick_id].keys()):
                predval = self.dict["sessioncache"][nick_id][predicate]
                self.aiml_kernel.setPredicate(predicate, predval, nick_id)

        # defaults
        if "nick" not in list(self.dict["sessioncache"][nick_id].keys()):
            self.dict["sessioncache"][nick_id]["nick"] = nick
            self.aiml_kernel.setPredicate("nick", nick, nick_id)

    def save_nick_session(self, nick, nick_id=None):
        if not nick_id:
            nick = Identifier(nick)
            nick_id = botusers.get_nick_id(nick, True)
        sessionData = self.aiml_kernel.getSessionData(nick_id)
        botdb.set_nick_value(nick, 'botai', sessionData)

    def save_brain(self):
        self.aiml_kernel.saveBrain(botconfig.config.aibrain)
        botsessiondata = self.aiml_kernel._botPredicates
        botdb.set_plugin_value('SpiceBot_AI', 'brain', botsessiondata)


botai = SpiceBot_AI()
