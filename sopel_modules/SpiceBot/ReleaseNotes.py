# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""This is a method to read files, online and local, and cache them"""

import os

from .Read import read as botread
from .Database import db as botdb


class BotNotes():

    def __init__(self):
        self.notes = botdb.get_plugin_value('SpiceBot_Release_Notes', 'notes') or dict()
        self.dir_to_scan = botread.get_config_dirs("SpiceBot_Release_Notes")
        self.load_txt_files(self.dir_to_scan)
        self.save_notes()

    def save_notes(self):
        savenotes = {}
        for notefile in list(self.notes.keys()):
            savenotes[notefile] = {"old": self.notes[notefile]["old"]}
        botdb.set_plugin_value('SpiceBot_Release_Notes', 'notes', savenotes)

    def load_txt_files(self, dir_to_scan):
        # iterate over files within
        for directory in dir_to_scan:
            for file in os.listdir(directory):
                filepath = os.path.join(directory, file)
                filepath = os.path.join(directory, file)
                if os.path.isfile(filepath) and filepath.endswith('.txt'):
                    # gather file stats
                    slashsplit = str(filepath).split("/")
                    filename = slashsplit[-1]
                    filename_base = str(os.path.basename(filename).rsplit('.', 1)[0]).lower()

                    if filename_base not in list(self.notes.keys()):
                        self.notes[filename_base] = {}
                    if "old" not in list(self.notes[filename_base].keys()):
                        self.notes[filename_base]["old"] = []
                    if "new" not in list(self.notes[filename_base].keys()):
                        self.notes[filename_base]["new"] = []

                    text_file = open(filepath, 'r')
                    lines = text_file.readlines()
                    for line in lines:
                        if str(line) not in self.notes[filename_base]["old"]:
                            self.notes[filename_base]["new"].append(str(line))
                            self.notes[filename_base]["old"].append(str(line))
                    text_file.close()


releasenotes = BotNotes()
