# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function

import sopel_modules.spicemanip as spicemanip

import re
from num2words import num2words


class Translate():

    def __init__(self):
        self.dict = {}

    def bot_translate_process(self, totranslate, translationtypes):

        # just in case
        if not isinstance(translationtypes, list):
            translationtypes = [translationtypes]

        for translationtype in translationtypes:

            if translationtype == "hyphen":
                totranslate = spicemanip.main(totranslate, 0).replace(' ', '-')

            elif translationtype == "underscore":
                totranslate = spicemanip.main(totranslate, 0).replace(' ', '_')

            elif translationtype == "ermahgerd":
                totranslate = self.trernslert(totranslate)

            elif translationtype == "obscure":
                totranslate = self.text_obscure(totranslate)

            elif translationtype == "piglatin":
                totranslate = self.text_piglatin(totranslate)

            elif translationtype == "binaryinvert":
                totranslate = self.text_binary_swap(totranslate)

            elif translationtype == "onetozero":
                totranslate = self.text_one_to_zero_swap(totranslate)

            elif translationtype == "upper":
                totranslate = spicemanip.main(totranslate, 0).upper()

            elif translationtype == "lower":
                totranslate = spicemanip.main(totranslate, 0).lower()

        return totranslate

    def text_obscure(self, words):
        amountofletters = len(words)
        mystring = "*" * amountofletters
        return mystring

    def text_piglatin(self, words):
        if not isinstance(words, list):
            words = [words]
        rebuildarray = []
        for word in words:
            word = word.lower()
            first = word[:1]
            if first in ['a', 'e', 'i', 'o', 'u']:
                new_word = word + 'ay'
            else:
                new_word = word[1:] + first + 'ay'
            rebuildarray.append(new_word)
        words = spicemanip.main(rebuildarray, 0)
        return words

    def trernslert(self, werds):
        terkerns = werds.split()
        er = ''
        for terk in terkerns:

            if terk.endswith(','):
                terk = re.sub(r"[,]+", '', terk)
                cermmer = 'true'
            else:
                cermmer = 'false'

            if terk.startswith('('):
                terk = re.sub(r"[(]+", '', terk)
                lerftperernthersers = 'true'
            else:
                lerftperernthersers = 'false'

            if terk.endswith(')'):
                terk = re.sub(r"[)]+", '', terk)
                rerghtperernthersers = 'true'
            else:
                rerghtperernthersers = 'false'

            if terk.endswith('%'):
                terk = re.sub(r"[%]+", '', terk)
                percernt = 'true'
            else:
                percernt = 'false'

            werd = self.ermergerd(terk)

            if lerftperernthersers == 'true':
                werd = str('(' + werd)

            if percernt == 'true':
                werd = str(werd + ' PERCERNT')

            if rerghtperernthersers == 'true':
                werd = str(werd + ')')

            if cermmer == 'true':
                werd = str(werd + ',')
            cermmer

            er = er + ' ' + werd
        return er

    def ermergerd(self, w):
        w = w.strip().lower()
        derctshernerer = {'me': 'meh', 'you': 'u', 'are': 'er', "you're": "yer", "i'm": "erm", "i've": "erv", "my": "mah", "the": "da", "omg": "ermahgerd"}
        if w in derctshernerer:
            return derctshernerer[w].upper()
        else:
            w = re.sub(r"[\.,/;:!@#$%^&*\?)(]+", '', w)
            if w[0].isdigit():
                w = num2words(int(w))
            w = re.sub(r"tion", "shun", w)
            pat = r"[aeiouy]+"
            er = re.sub(pat, "er", w)
            if w.startswith('y'):
                er = 'y' + re.sub(pat, "er", w[1:])
            if w.endswith('e') and not w.endswith('ee') and len(w) > 3:
                er = re.sub(pat, "er", w[:-1])
            if w.endswith('ing'):
                er = re.sub(pat, "er", w[:-3]) + 'in'
            er = er[0] + er[1:].replace('y', 'er')
            er = er.replace('rr', 'r')
            return er.upper()

    def text_one_to_zero_swap(self, words):
        if not words or words == []:
            return "No input provided"
        if not isinstance(words, list):
            words = [words]
        words = spicemanip.main(words, 0).split(" ")
        outputarray = []
        for word in words:
            if not self.isitbinary(word):
                word = self.text_binary_swap(word)
            word = str(word).replace('1', '2')
            word = str(word).replace('0', '1')
            word = str(word).replace('2', '0')
            outputarray.append(str(word))
        outputarray = spicemanip.main(outputarray, 0)
        return outputarray

    def text_binary_swap(self, words):
        if not words or words == []:
            return "No input provided"
        if not isinstance(words, list):
            words = [words]
        words = spicemanip.main(words, 0).split(" ")
        outputarray = []
        for word in words:
            if self.isitbinary(word):
                word = self.bits2string(word) or 'error'
            else:
                word = self.string2bits(word) or 1
                word = spicemanip.main(word, 0)
            outputarray.append(str(word))
        outputarray = spicemanip.main(outputarray, 0)
        return outputarray

    def unicode_string_cleanup(string):
        for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "...")):
            string = string.replace(*r)
        return string

    def isitbinary(self, string):
        p = set(string)
        s = {'0', '1'}
        if s == p or p == {'0'} or p == {'1'}:
            return True
        else:
            return False

    def string2bits(self, s=''):
        return [bin(ord(x))[2:].zfill(8) for x in s]

    def bits2string(self, b=None):
        return ''.join(chr(int(b[i*8:i*8+8], 2)) for i in range(len(b)//8))


translate = Translate()
