# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system. Based On Chatty cathy
"""

from sopel.tools import Identifier
from sopel.config.types import StaticSection, ListAttribute

import os
import tempfile
import aiml

from .Database import db as botdb
from .Logs import logs


class SpiceBot_AI_MainSection(StaticSection):
    extra = ListAttribute('extra')


class SpiceBot_AI():

    def __init__(self):
        self.load_commands = [0]
        self.braindirs = []
        self.dict = {
                    "counts": 0,
                    "failcounts": 0,
                    "sessioncache": {}
                    }
        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()

        # aiml parser
        self.aiml_parser = aiml.AimlParser.create_parser()

        # Don't warn for no matches
        self.aiml_kernel._verboseMode = False

        # Learn responses
        self.load_brain()

    def load_brain(self):
        import sopel_modules
        braindirs = []
        for plugin_dir in set(sopel_modules.__path__):
            configsdir = os.path.join(plugin_dir, "SpiceBot_Configs")
            aimldir = os.path.join(configsdir, "aiml")
            braindirs.append(aimldir)

        # learn directories
        self.learn(braindirs)

    def load_extras(self, bot):
        if len(bot.config.SpiceBot_AI.extra):
            self.learn(self, bot.config.SpiceBot_AI.extra)

    def learn(self, braindirs):
        for braindir in braindirs:
            if braindir not in self.braindirs:
                self.braindirs.append(braindir)
                dirnumber = max(self.load_commands) + 1
                self.load_commands.append(dirnumber)
                tempbrain = tempfile.mkstemp()[1]
                with open(tempbrain, 'w') as fileo:
                    fileo.write(
                        "<aiml version='1.0.1' encoding='UTF-8'>"
                        "    <!-- std-startup.xml -->\n"
                        "    <category>\n"
                        "        <pattern>LOAD AIML {}</pattern>\n"
                        "        <template>\n"
                        "            <learn>{}</learn>\n"
                        "        </template>\n"
                        "    </category>\n"
                        "</aiml>".format(str(dirnumber), os.path.join(braindir, "*"))
                    )
                self.aiml_kernel.learn(tempbrain)
        for number in self.load_commands:
            if number != 0:
                self.aiml_kernel.respond("LOAD AIML {}").format(str(dirnumber))
                os.remove(tempbrain)

    def on_message(self, bot, trigger, message):
        nick = Identifier(trigger.nick)
        nick_id = botdb.get_nick_id(nick, create=True)
        self.check_user_import(nick, nick_id)
        aiml_response = self.aiml_kernel.respond(message, nick_id)
        self.save_nick_session(nick, nick_id)
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

    def save_nick_session(self, nick, nick_id=None):
        if not nick_id:
            nick = Identifier(nick)
            nick_id = botdb.get_nick_id(nick, create=True)
        sessionData = self.aiml_kernel.getSessionData(nick_id)
        botdb.set_nick_value(nick, 'botai', sessionData)

    def check_file_parse(self, parsefile):
        try:
            self.aiml_parser.parse(parsefile)
            self.dict["counts"] += 1
        except Exception as e:
            logs.log('SpiceBot_AI', "Error loading %s: %s (%s)" % ('aiml', e, parsefile))
            self.dict["failcounts"] += 1


botai = SpiceBot_AI()
