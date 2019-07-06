# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Reddit system.
"""

from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.formatting import bold, color, colors

from sopel_modules.spicemanip import spicemanip

import datetime as dt
import praw
import prawcore
from random import randint

from .Config import config as botconfig
from .Logs import logs


class SpiceBot_Reddit_MainSection(StaticSection):
    client_id = ValidatedAttribute('client_id', default=None)
    client_secret = ValidatedAttribute('client_secret', default=None)


class BotReddit():
    """This Logs all channels known to the server"""
    def __init__(self):
        self.setup_reddit()
        self.cache = {}
        self.client_id = botconfig.SpiceBot_Reddit.client_id
        self.client_secret = botconfig.SpiceBot_Reddit.client_secret
        if not self.client_id or not self.client_secret:
            self.praw = None
            logs.log('SpiceBot_Reddit', "Client ID or Secret missing from config", True)
        else:
            self.praw = praw.Reddit(
                                    client_id=self.client_id,
                                    client_secret=self.client_secret,
                                    user_agent='spicebot:net.example.myredditapp:v1.2.3 (by /u/SpiceBot-dbb)'
                                    )

    def setup_reddit(self):
        botconfig.define_section("SpiceBot_Reddit", SpiceBot_Reddit_MainSection, validate=False)

    def prerun(self, trigger):
        if not self.praw:
            return "Reddit API is not available"
        message = "if you see this, there may be an error"
        trigger_argsdict = self.trigger_handler(trigger)
        if trigger_argsdict["slashcomm"] == "u":
            return self.user_handler(trigger_argsdict)
        elif trigger_argsdict["slashcomm"] == "r":
            return self.subreddit_handler(trigger_argsdict)
        return message

    def user_handler(self, trigger_argsdict):
        subcommand_valid = ['check']
        subcommand = spicemanip([x for x in trigger_argsdict["args"] if x in subcommand_valid], 1) or 'check'

        userreal = self.reddit_user_exists(trigger_argsdict["command"])
        if not userreal["exists"]:
            return userreal["error"]

        fulluurul = str("https://www.reddit.com/" + trigger_argsdict["slashcomm"] + "/" + trigger_argsdict["command"])
        if subcommand == 'check':
            u = self.praw.redditor(trigger_argsdict["command"])
            message = ['[REDDITOR] ' + u.name]
            is_cakeday = self.user_cakeday(u.created_utc)
            if is_cakeday:
                message.append(bold(color('Cake day', colors.LIGHT_PURPLE)))
            message.append(fulluurul)
            if u.is_gold:
                message.append(bold(color('Gold', colors.YELLOW)))
            if u.is_mod:
                message.append(bold(color('Mod', colors.GREEN)))
            message.append('Link: ' + str(u.link_karma))
            message.append('Comment: ' + str(u.comment_karma))
            return message

    def user_cakeday(self, created):
        now = dt.datetime.utcnow()
        cakeday_start = dt.datetime.utcfromtimestamp(created)
        cakeday_start = cakeday_start.replace(year=now.year)
        day = dt.timedelta(days=1)
        year_div_by_400 = now.year % 400 == 0
        year_div_by_100 = now.year % 100 == 0
        year_div_by_4 = now.year % 4 == 0
        is_leap = year_div_by_400 or ((not year_div_by_100) and year_div_by_4)
        if (not is_leap) and ((cakeday_start.month, cakeday_start.day) == (2, 29)):
            # If cake day is 2/29 and it's not a leap year, cake day is 3/1.
            # Cake day begins at exact account creation time.
            is_cakeday = cakeday_start + day <= now <= cakeday_start + (2 * day)
        else:
            is_cakeday = cakeday_start <= now <= cakeday_start + day
        return is_cakeday

    def subreddit_handler(self, trigger_argsdict):
        subcommand_valid = ['check', 'hot', 'new', 'top', 'random', 'controversial', 'gilded', 'rising', 'best']
        subcommand = spicemanip([x for x in trigger_argsdict["args"] if x in subcommand_valid], 1) or 'check'

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
            targnum = spicemanip([x for x in trigger_argsdict["args"] if str(x).isdigit()], 1) or 500
        else:
            targnum = spicemanip([x for x in trigger_argsdict["args"] if str(x).isdigit()], 1) or 1
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
        trigger_args = spicemanip(trigger.args[1], 'create')
        trigger_argsdict = {
                        "slashcomm": spicemanip(trigger_args, 1).lower()[:1],
                        "command": spicemanip(trigger_args, 1).lower()[2:],
                        "args": spicemanip(trigger_args, "2+", 'list')
                        }
        if trigger_argsdict["slashcomm"] == "u":
            trigger_argsdict["urltypetxt"] = "user"
        if trigger_argsdict["slashcomm"] == "r":
            trigger_argsdict["urltypetxt"] = "subreddit"

        return trigger_argsdict

    def reddit_subreddit_check(self, sub):
        returndict = {"exists": True, "error": None}
        try:
            self.praw.subreddits.search_by_name(sub, exact=True)
        except prawcore.exceptions.NotFound:
            returndict["error"] = str(sub + " appears to not exist!")
            returndict["exists"] = False
            return returndict

        try:
            subtype = self.praw.subreddit(sub).subreddit_type
            returndict["subtype"] = subtype
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
        return returndict

    def reddit_user_exists(self, user):
        returndict = {"exists": True, "error": None}
        try:
            self.praw.redditor(user).fullname
        except prawcore.exceptions.NotFound:
            returndict["exists"] = False
            returndict["error"] = str(user + " appears to not exist!")
            return returndict
        return returndict


reddit = BotReddit()
