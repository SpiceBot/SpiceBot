# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system. Based On Chatty cathy
"""

from sopel.tools import Identifier

import os
import tempfile
import aiml

from .Config import config as botconfig


class SpiceBot_AI():

    def __init__(self):
        self.dict = {
                    "counts": 0,
                    }
        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()

        # Don't warn for no matches
        self.aiml_kernel._verboseMode = False

        # Learn responses
        self.load_brain()

    def load_brain(self):
        if os.path.isfile(botconfig.config.aibrain):
            self.aiml_kernel.bootstrap(brainFile=botconfig.config.aibrain)
            self.aiml_kernel.respond("LOAD AIML B")
        else:
            import sopel_modules
            for plugin_dir in set(sopel_modules.__path__):
                configsdir = os.path.join(plugin_dir, "SpiceBot_Configs")
                aimldir = os.path.join(configsdir, "aiml")
                aimlstarter = tempfile.mkstemp()[1]
                with open(aimlstarter, 'w') as fileo:
                    fileo.write(
                        "<aiml version='1.0.1' encoding='UTF-8'>"
                        "    <!-- std-startup.xml -->\n"
                        "    <category>\n"
                        "        <pattern>LOAD AIML B</pattern>\n"
                        "        <template>\n"
                        "            <learn>{}</learn>\n"
                        "        </template>\n"
                        "    </category>\n"
                        "</aiml>".format(os.path.join(aimldir, "*"))
                    )
                self.aiml_kernel.learn(aimlstarter)
                self.aiml_kernel.respond("LOAD AIML B")
                os.remove(aimlstarter)
            self.save_brain()

    def save_brain(self):
        self.aiml_kernel.saveBrain(botconfig.config.aibrain)

    def on_message(self, bot, trigger, message):
        nick = Identifier(trigger.nick)
        nick_id = bot.db.get_nick_id(nick, create=True)
        aiml_response = self.aiml_kernel.respond(message, nick_id)
        return aiml_response


botai = SpiceBot_AI()
