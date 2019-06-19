# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Reddit system.
"""

from sopel.config.types import StaticSection, ValidatedAttribute

import spicemanip

import requests
# from lxml import html
from fake_useragent import UserAgent
import praw
from prawcore import NotFound
from random import randint

from .Config import config as botconfig
from .Logs import logs


class SpiceBot_Reddit_MainSection(StaticSection):
    client_id = ValidatedAttribute('client_id', default=None)
    client_secret = ValidatedAttribute('client_secret', default=None)


class BotReddit():
    """This Logs all channels known to the server"""
    def __init__(self):
        self.setup_commands()
        self.dict = {}
        self.header = {'User-Agent': str(UserAgent().chrome)}
        self.client_id = botconfig.SpiceBot_Reddit.client_id
        self.client_secret = botconfig.SpiceBot_Reddit.client_secret
        if not self.client_id or not self.client_secret:
            self.praw = None
            logs.log('SpiceBot_Reddit', "Error loading reddit auth", True)
        else:
            self.praw = praw.Reddit(
                                    client_id=self.client_id,
                                    client_secret=self.client_secret,
                                    user_agent='spicebot:net.example.myredditapp:v1.2.3 (by /u/SpiceBot-dbb)'
                                    )

    def setup_commands(self):
        botconfig.define_section("SpiceBot_Reddit", SpiceBot_Reddit_MainSection, validate=False)

    def prerun(self, trigger):
        if not self.praw:
            return "Reddit API is not available"
        message = "if you see this, there may be an error"
        trigger_argsdict = self.trigger_handler(trigger)
        page = self.check_reddit_up()
        if not page:
            message = "Reddit Appears to be down"
            return message
        elif str(page.status_code).startswith(tuple(["4", "5"])):
            message = "Reddit is replying with http code " + str(page.status_code)
            return message
        if trigger_argsdict["slashcomm"] == "u":
            return self.user_handler(trigger_argsdict)
        elif trigger_argsdict["slashcomm"] == "r":
            return self.subreddit_handler(trigger_argsdict)
        return message

    def user_handler(self, trigger_argsdict):
        subcommand_valid = ['check']
        subcommand = spicemanip.main([x for x in trigger_argsdict["args"] if x in subcommand_valid], 1) or 'check'

        userreal = self.reddit_user_exists(trigger_argsdict["command"])
        if not userreal["exists"]:
            return userreal["error"]

        fulluurul = str("https://www.reddit.com/" + trigger_argsdict["slashcomm"] + "/" + trigger_argsdict["command"])
        if subcommand == 'check':
            return [trigger_argsdict["command"] + " appears to be a valid reddit " + trigger_argsdict["urltypetxt"] + "!", fulluurul]

    def subreddit_handler(self, trigger_argsdict):
        subcommand_valid = ['check', 'hot', 'new', 'top', 'random', 'controversial', 'gilded', 'rising', 'best']
        subcommand = spicemanip.main([x for x in trigger_argsdict["args"] if x in subcommand_valid], 1) or 'check'

        fullrurul = str("https://www.reddit.com/" + trigger_argsdict["slashcomm"] + "/" + trigger_argsdict["command"])

        subredditcheck = self.reddit_subreddit_check(trigger_argsdict["command"])
        if not subredditcheck["exists"]:
            return subredditcheck["error"]

        subreddit = self.praw.subreddit(trigger_argsdict["command"])
        if subcommand == 'check':
            dispmsg = []
            dispmsg.append("[Reddit " + trigger_argsdict["slashcomm"] + "/" + trigger_argsdict["command"] + "]")
            if subreddit.over18:
                dispmsg.append("<NSFW>")
            dispmsg.append(str(subreddit.public_description))
            dispmsg.append(fullrurul)
            return dispmsg

        if subcommand == 'random':
            targnum = spicemanip.main([x for x in trigger_argsdict["args"] if str(x).isdigit()], 1) or 500
        else:
            targnum = spicemanip.main([x for x in trigger_argsdict["args"] if str(x).isdigit()], 1) or 1
        targnum = int(targnum)

        if subcommand == 'new':
            submissions = subreddit.new(limit=targnum)
        elif subcommand == 'top':
            submissions = subreddit.top(limit=targnum)
        elif subcommand == 'hot':
            submissions = subreddit.hot(limit=targnum)
        elif subcommand == 'controversial':
            submissions = subreddit.controversial(limit=targnum)
        elif subcommand == 'gilded':
            submissions = subreddit.gilded(limit=targnum)
        elif subcommand == 'rising':
            submissions = subreddit.rising(limit=targnum)
        elif subcommand == 'random':
            submissions = subreddit.hot(limit=targnum)
        else:
            return "An error has occured."

        listarray = []
        for submission in submissions:
            listarray.append(submission)

        if listarray == []:
            submission = None
        elif subcommand == 'random':
            submission = listarray[randint(0, len(listarray) - 1)]
        else:
            submission = listarray[targnum - 1]

        dispmsg = []
        dispmsg.append("[Reddit " + trigger_argsdict["slashcomm"] + "/" + trigger_argsdict["command"] + " " + subcommand + "]")
        if subreddit.over18:
            dispmsg.append("<NSFW>")
        if submission:
            dispmsg.append("{" + str(submission.score) + "}")
            dispmsg.append(submission.title)
            dispmsg.append(submission.url)
        else:
            dispmsg.append("No Content Found.")
        return dispmsg

    def trigger_handler(self, trigger):
        trigger_args = spicemanip.main(trigger.args[1], 'create')
        trigger_argsdict = {
                        "slashcomm": spicemanip.main(trigger_args, 1).lower()[:1],
                        "command": spicemanip.main(trigger_args, 1).lower()[2:],
                        "args": spicemanip.main(trigger_args, "2+", 'list')
                        }
        if trigger_argsdict["slashcomm"] == "u":
            trigger_argsdict["urltypetxt"] = "user"
        if trigger_argsdict["slashcomm"] == "r":
            trigger_argsdict["urltypetxt"] = "subreddit"

        return trigger_argsdict

    def check_reddit_up(self):
        try:
            page = requests.get("https://www.reddit.com/", headers=self.header)
        except Exception as e:
            page = e
            page = None
        return page

    def reddit_subreddit_check(self, sub):
        returndict = {"exists": True, "error": None}
        try:
            self.praw.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            returndict["error"] = str(sub + " appears to not exist!")
            returndict["exists"] = False
            return returndict

        try:
            subtype = self.praw.subreddit(sub).subreddit_type
        except Exception as e:
            returndict["exists"] = False
            if str(e) == "received 403 HTTP response":
                returndict["error"] = str(sub + " appears to be an private subreddit!")
                return returndict
            elif str(e) == "received 404 HTTP response":
                returndict["error"] = str(sub + " appears to be an banned subreddit!")
                return returndict
            else:
                returndict["error"] = str(sub + " appears to not have a type")
                return returndict
        return subtype

        return returndict

    def reddit_user_exists(self, user):
        returndict = {"exists": True, "error": None}
        try:
            self.praw.redditor(user).fullname
        except NotFound:
            returndict["exists"] = False
            returndict["error"] = str(user + " appears to not exist!")
            return returndict
        return returndict


reddit = BotReddit()
