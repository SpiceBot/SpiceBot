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
            if plugin_dir in ["SpiceBot_Configs"]:
                for pathname in os.listdir(plugin_dir):
                    if pathname in ["aiml"]:
                        pathpath = os.path.join(plugin_dir, pathname)
                        for aimlfile in os.listdir(pathpath):
                            aiml_filename = os.path.join(pathpath, pathname)
                            self.aiml_kernel.learn(aiml_filename)

    def on_message(self, message):
        return self.aiml_kernel.respond(message.content)
