# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Reddit system.
"""

import spicemanip

import requests
from fake_useragent import UserAgent


class BotReddit():
    """This Logs all channels known to the server"""
    def __init__(self):
        self.dict = {}
        self.header = {'User-Agent': str(UserAgent().chrome)}

    def prerun(self, trigger):
        # trigger_argsdict = self.trigger_handler(trigger)
        page = self.check_reddit_up()
        if not page:
            message = "Reddit Appears to be down"
            return message
        elif str(page.status_code).startswith(tuple(["4", "5"])):
            message = "Reddit is replying with http code " + str(page.status_code)
            return message

        message = "Reddit is replying with http code " + str(page.status_code)
        return message

    def trigger_handler(self, trigger):
        trigger_args = spicemanip.main(trigger.args[1], 'create')
        trigger_argsdict = {
                        "slashcomm": spicemanip.main(trigger_args, 1).lower()[:1],
                        "command": spicemanip.main(trigger_args, 1).lower()[2:],
                        "args": spicemanip.main(trigger_args, "2+", 'list')
                        }
        return trigger_argsdict

    def check_reddit_up(self):
        try:
            page = requests.get("https://www.reddit.com/", headers=self.header)
        except Exception as e:
            page = e
            page = None
        return page


reddit = BotReddit()
