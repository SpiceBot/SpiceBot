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


class SpiceBot_AI_MainSection(StaticSection):
    extra = ListAttribute('extra')
    gender = ValidatedAttribute('gender', default='female')


class SpiceBot_AI():

    def __init__(self):
        self.setup_ai()
        self.braindirs = []
        self.dict = {
                    "counts": 0,
                    "failcounts": 0,
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
        import sopel_modules
        braindirs = []
        for plugin_dir in set(sopel_modules.__path__):
            configsdir = os.path.join(plugin_dir, "SpiceBot_Configs")
            aimldir = os.path.join(configsdir, "aiml")
            braindirs.append(aimldir)

        if len(botconfig.SpiceBot_AI.extra):
            for extrabraindir in botconfig.SpiceBot_AI.extra:
                braindirs.append(extrabraindir)

        # learn directories
        self.learn(braindirs)
        self.save_brain()

    def load_bot_values(self):
        self.aiml_kernel.setBotPredicate("nick", botconfig.nick)
        # self.aiml_kernel.setBotPredicate("gender", botconfig.SpiceBot_AI.gender)
        self.aiml_kernel.setBotPredicate("gender", "male")

    def learn(self, braindirs):
        for braindir in braindirs:
            if braindir not in self.braindirs:
                self.braindirs.append(braindir)
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
        nick_id = botdb.get_nick_id(nick, create=True)
        self.check_user_import(nick, nick_id)

        message = self.bot_message_precipher(bot, trigger, message)
        aiml_response = self.aiml_kernel.respond(message, nick_id)
        aiml_response = self.bot_message_decipher(bot, trigger, aiml_response)

        self.save_nick_session(nick, nick_id)
        self.save_brain()

        return aiml_response

    def bot_message_precipher(self, bot, trigger, message):
        message = message.upper()
        puct_dict = {"!": "exclamationmark", ".": "period", "?": "questionmark", ",": "comma"}
        for puctuation in puct_dict.keys():
            message = message.replace(puctuation, puct_dict[puctuation])
        for botitem in ["nick"]:
            message = message.replace(str(eval("bot." + botitem)).upper(), str("bot" + botitem).upper())
        for triggeritem in ["nick", "sender"]:
            message = message.replace(str(eval("trigger." + triggeritem)).upper(), str("trigger" + triggeritem).upper())
        return message

    def bot_message_decipher(self, bot, trigger, aiml_response):
        for botitem in ["nick"]:
            aiml_response = aiml_response.replace("bot" + botitem, str(eval("bot." + botitem)))
        for triggeritem in ["nick", "sender"]:
            aiml_response = aiml_response.replace("trigger" + triggeritem, str(eval("trigger." + triggeritem)))
        return aiml_response

    def check_user_import(self, nick, nick_id=None):
        if not nick_id:
            nick = Identifier(nick)
            nick_id = botdb.get_nick_id(nick, create=True)
        if nick_id not in self.dict["sessioncache"].keys():
            self.dict["sessioncache"][nick_id] = botdb.get_nick_value(nick, 'botai') or {}
            for predicate in self.dict["sessioncache"][nick_id].keys():
                predval = self.dict["sessioncache"][nick_id][predicate]
                self.aiml_kernel.setPredicate(predicate, predval, nick_id)

        # defaults
        if "nick" not in self.dict["sessioncache"][nick_id].keys():
            self.dict["sessioncache"][nick_id]["nick"] = nick
            self.aiml_kernel.setPredicate("nick", nick, nick_id)

    def save_nick_session(self, nick, nick_id=None):
        if not nick_id:
            nick = Identifier(nick)
            nick_id = botdb.get_nick_id(nick, create=True)
        sessionData = self.aiml_kernel.getSessionData(nick_id)
        botdb.set_nick_value(nick, 'botai', sessionData)

    def save_brain(self):
        self.aiml_kernel.saveBrain(botconfig.config.aibrain)


botai = SpiceBot_AI()
