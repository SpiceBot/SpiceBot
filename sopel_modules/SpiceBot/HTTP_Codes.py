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

    def fetch_result(self, query):
        returndict = {
                        "basic": "",
                        "explanation": "",
                        }
        if not re.match('^[1-5]\d{2}$', query):
            returndict["basic"] = "Invalid HTTP status code:"
            returndict["explanation"] = str(query)
            return returndict

        url = self.api_url + query
        try:
            r = requests.get(url=url, timeout=(10.0, 4.0))
        except requests.exceptions.ConnectTimeout:
            returndict["basic"] = "Connection timed out."
            return returndict
        except requests.exceptions.ConnectionError:
            returndict["basic"] = "Couldn't connect to server."
            return returndict
        except requests.exceptions.ReadTimeout:
            returndict["basic"] = "Server took too long to send data."
            return returndict
        if r.status_code == 404:
            returndict["basic"] = "Unknown HTTP status code:"
            returndict["explanation"] = str(query)
            return returndict
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            returndict["basic"] = "HTTP error:"
            returndict["explanation"] = str(e.message)
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
            returndict["basic"] = "An Error Occured:"
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

        return returndict


httpcodes = Bothttpcodes()
