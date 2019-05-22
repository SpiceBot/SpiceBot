# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Commands system.

This Class stores commands in an easy to access manner
"""

import spicemanip


class BotCommands():
    """This Logs all commands known to the bot"""
    def __init__(self):
        self.dict = {
                    "counts": 0,
                    "commands": {
                                'module': {},
                                'nickname': {},
                                'rule': {}
                                },
                    "nickrules": []
                    }

    def commandsquery_register(self, bot, command_type, validcoms, aliasfor=None):

        if not isinstance(validcoms, list):
            validcoms = [validcoms]

        if command_type not in self.dict['commands'].keys():
            self.dict['commands'][command_type] = dict()
        self.dict['counts'] += 1

        dict_from_file = dict()

        # default command to filename
        if "validcoms" not in dict_from_file.keys():
            dict_from_file["validcoms"] = validcoms

        if not aliasfor:

            maincom = dict_from_file["validcoms"][0]
            if len(dict_from_file["validcoms"]) > 1:
                comaliases = spicemanip.main(dict_from_file["validcoms"], '2+', 'list')
            else:
                comaliases = []
            self.dict['commands'][command_type][maincom] = dict_from_file
        else:
            comaliases = validcoms

        for comalias in comaliases:
            if comalias not in self.dict['commands'][command_type].keys():
                self.dict['commands'][command_type][comalias] = {"aliasfor": aliasfor}


commands = BotCommands()
