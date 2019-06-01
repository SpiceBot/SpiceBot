# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system. Based On Chatty cathy
"""

import os
import tempfile
import aiml


class SpiceBot_AI():

    def __init__(self):
        self.dict = {
                    "counts": 0,
                    }
        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()

        # self.aiml_kernel._verboseMode = False
        # Learn responses
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

    def on_message(self, message):
        aiml_response = self.aiml_kernel.respond(message)
        return aiml_response


botai = SpiceBot_AI()
