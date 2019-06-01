# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system. Based On Chatty cathy
"""

from sopel.tools import Identifier

import os
import tempfile
import aiml

from .Database import db as botdb


class SpiceBot_AI():

    def __init__(self):
        self.dict = {
                    "counts": 0,
                    "sessioncache": {}
                    }
        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()

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

        # TODO add extra config

        for braindir in braindirs:
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
                    "</aiml>".format(os.path.join(braindir, "*"))
                )
            self.aiml_kernel.learn(tempbrain)
            self.aiml_kernel.respond("LOAD AIML B")
            os.remove(tempbrain)

    def on_message(self, bot, trigger, message):
        nick = Identifier(trigger.nick)
        nick_id = bot.db.get_nick_id(nick, create=True)
        if nick_id not in self.dict["sessioncache"].keys():
            self.dict["sessioncache"][nick_id] = botdb.get_nick_value(nick, 'botai') or {}
            for predicate in self.dict["sessioncache"][nick_id].keys():
                predval = self.dict["sessioncache"][nick_id][predicate]
                self.aiml_kernel.setPredicate(predicate, predval, nick_id)
        aiml_response = self.aiml_kernel.respond(message, nick_id)
        sessionData = self.aiml_kernel.getSessionData(nick_id)
        botdb.set_nick_value(nick, 'botai', sessionData)
        return aiml_response


botai = SpiceBot_AI()
