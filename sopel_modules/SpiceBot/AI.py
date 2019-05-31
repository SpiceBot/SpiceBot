# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot AI system. Based On Chatty cathy
"""

import os
import aiml

BOT_PREFIX = (".", '?', '!')


class SpiceBot_AI():

    def __init__(self):
        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()
        # Learn responses
        import sopel_modules
        for plugin_dir in set(sopel_modules.__path__):
            configsdir = os.path.join(plugin_dir, "SpiceBot_Configs")
            aimldir = os.path.join(configsdir, "aiml")
            for aimlfile in os.listdir(aimldir):
                aiml_filename = os.path.join(aimldir, aimlfile)
                self.aiml_kernel.learn(aiml_filename)

    def on_message(self, message):
        return self.aiml_kernel.respond(message.content)
