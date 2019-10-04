# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot HTTP Codes system.
"""

import re
import requests
from lxml import html


class Bothttpcodes():

    def __init__(self):
        self.api_url = 'https://httpstatuses.com/'
        self.basic_xpath = "/html/body/article/h1[1]/text()"
        self.explain_xpath = "/html/body/article/p[1]/text()"
        self.cache = {}

    def fetch_result(self, query):

        query = str(query)

        if not query:
            return {
                    "query": "",
                    "basic": "An Error Occured",
                    "explanation": "You must provide a HTTP status code to look up.",
                    "error": True
                    }

        # check cache
        cached = self.check_cache(query)
        if cached:
            return cached

        returndict = {
                        "query": query,
                        "basic": "",
                        "explanation": "",
                        "error": False
                        }

        if not re.match('^[1-5]\d{2}$', query):
            returndict["error"] = True
            returndict["basic"] = "An Error Occured"
            returndict["explanation"] = "Invalid HTTP status code: %s" % query
            self.add_to_cache(returndict)
            return returndict

        url = self.api_url + query
        try:
            r = requests.get(url=url, timeout=(10.0, 4.0))
        except requests.exceptions.ConnectTimeout:
            returndict["error"] = True
            returndict["basic"] = "An Error Occured"
            returndict["explanation"] = "Connection timed out."
            return returndict
        except requests.exceptions.ConnectionError:
            returndict["error"] = True
            returndict["basic"] = "An Error Occured"
            returndict["explanation"] = "Couldn't connect to server."
            return returndict
        except requests.exceptions.ReadTimeout:
            returndict["error"] = True
            returndict["basic"] = "An Error Occured"
            returndict["explanation"] = "Server took too long to send data."
            return returndict
        if r.status_code == 404:
            returndict["error"] = True
            returndict["basic"] = "An Error Occured"
            returndict["explanation"] = "Unknown HTTP status code: %s" % query
            self.add_to_cache(returndict)
            return returndict
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            returndict["error"] = True
            returndict["basic"] = "An Error Occured"
            returndict["basic"] = "HTTP error: %s" % str(e.message)
            self.add_to_cache(returndict)
            return returndict

        tree = html.fromstring(r.content)
        try:
            title = tree.xpath((self.basic_xpath))
            if isinstance(title, list):
                title = title[0]
        except Exception as e:
            title = None
        if title:
            returndict["basic"] = str(title)
        else:
            returndict["error"] = True
            returndict["basic"] = "An Error Occured"
            returndict["explanation"] = "Xpath for basic yeilded no information"
            return returndict

        try:
            explanation = tree.xpath((self.explain_xpath))
            if isinstance(explanation, list):
                explanation = explanation[0]
        except Exception as e:
            explanation = None
        if explanation:
            returndict["explanation"] = str(explanation)
        else:
            returndict["explanation"] = "Xpath for explanation yeilded no information"

        self.add_to_cache(returndict)
        return returndict

    def add_to_cache(self, cachedict):
        if cachedict["query"] not in list(self.cache.keys()):
            self.cache[cachedict["query"]] = {
                                                "query": cachedict["query"],
                                                "basic": cachedict["basic"],
                                                "explanation": cachedict["explanation"],
                                                }

    def check_cache(self, query):
        if query not in list(self.cache.keys()):
            return None
        return self.cache[query]


httpcodes = Bothttpcodes()
