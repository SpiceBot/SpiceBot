#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Top-level package for spicemanip."""

__author__ = """Sam Zick"""
__email__ = 'sam@deathbybandaid.net'
__version__ = '0.1.8'

import random
import collections


# TODO 'this*that' or '1*that' replace either all strings matching, or an index value
# TODO reverse sort z.sort(reverse = True)
# list.extend adds lists to eachother


class Spicemanip():
    def __init__(self):
        pass

    def __call__(self, inputs, task, output_type='default'):

        if hasattr(self, str(task)):
            raise Exception(
                str(self.task) + " is not a valid spicemanip function.")

        # convert input into list
        self.inputs = inputs
        self.core_input_handler()

        # determine task
        self.task = task
        self.core_task_handler()

        # determine output of list
        self.output_type = output_type
        self.core_output_handler()

        # return value/s
        return self.outputs

    def core_input_handler(self):
        # Input needs to be a list, but don't split a word into letters
        if not self.inputs:
            self.input_list = []
        if isinstance(self.inputs, list):
            self.input_list = list(self.inputs)
        if isinstance(self.inputs, collections.abc.KeysView):
            self.input_list = list(self.inputs)
        if isinstance(self.inputs, dict):
            self.input_list = list(self.inputs.keys())
        if not isinstance(self.inputs, list):
            self.input_list = list(self.inputs.split(" "))

    def core_task_handler(self):

        # Create return
        if self.task in ['create']:
            self.outputs = self.input_list
            return

        if len(self.input_list):

            if self.task in ["0", 0, 'complete']:
                self.outputs = self.string(self.input_list)
                return

            elif self.task in ['index']:
                self.outputs = self.index(
                    self.input_list[0], self.input_list[1], self.input_list[2])

            elif self.task.isdigit():
                self.outputs = self.number(self.input_list, int(self.task))

            elif self.task in ['last', '-1', -1]:
                self.outputs = self.number(self.input_list, -1)

            elif "^" in str(self.task):
                range_start, range_end = str(self.task).split("^", 1).sort()
                self.outputs = self.rangebetween(self.input_list, range_start,
                                                 range_end)

            elif str(self.task).startswith("split_"):
                self.outputs = self.split(self.input_list,
                                          str(self.task).replace("split_", ""))

            elif str(self.task).endswith("!"):
                self.outputs = self.exclude(self.input_list,
                                            str(self.task).replace("!", ""))

            elif str(self.task).endswith("+"):
                self.outputs = self.incrange_plus(
                    self.input_list,
                    str(self.task).replace("+", ""))

            elif str(self.task).endswith("-"):
                self.outputs = self.incrange_minus(
                    self.input_list,
                    str(self.task).replace("-", ""))

            elif str(self.task).endswith(">"):
                self.outputs = self.excrange_plus(
                    self.input_list,
                    str(self.task).replace(">", ""))

            elif str(self.task).endswith("<"):
                self.outputs = self.excrange_minus(
                    self.input_list,
                    str(self.task).replace("<", ""))

            elif hasattr(self,
                         str(self.task)) and not str(self.task).startswith("core_"):
                self.outputs = eval('self.' + str(self.task) + '(self.input_list)')

            else:
                raise Exception(
                    str(self.task) + " is not a valid spicemanip function.")

    def core_output_handler(self):

        core_defaults = {
                        'string': "string",
                        'number': "string",
                        'rangebetween': "string",
                        'exclude': "string",
                        'random': "string",
                        'incrange_plus': "string",
                        'incrange_minus': "string",
                        'excrange_plus': "string",
                        'excrange_minus': "string",
                        'count': "dict"
                        }

        # default return if not specified
        if self.output_type == 'default':
            if self.task in list(core_defaults.keys()):
                self.output_type = core_defaults[self.task]

        # verify output is correct
        if self.output_type in ['return', 'dict']:
            return

        if self.output_type == 'string':
            self.outputs = self.string(self.outputs)
            return

        if self.output_type in ['list', 'array']:
            self.outputs = self.list(self.outputs)
            return

    # Convert list to string
    def string(self, inputs):
        if not isinstance(inputs, list):
            return inputs
        if not inputs or not len(inputs):
            return ''
        return ' '.join(inputs)

    # Convert inputs to list
    def list(self, inputs):
        if isinstance(inputs, list):
            return inputs
        if not inputs or not len(inputs):
            return []
        return list(inputs.split(" "))

    def index(self, indexitem, listtoindex, listtocompare):
        for x, y in zip(listtoindex, listtocompare):
            if x == indexitem:
                return y
        return ''

    # Get number item from list
    def number(self, inputs, index_number):
        if int(index_number) > 0:
            index_number -= 1
        try:
            return inputs[int(index_number)]
        except IndexError:
            return ''

    # range between items in list
    def rangebetween(self, inputs, range_start, range_end):
        range_start, range_end = int(range_start), int(range_end)
        if range_end == range_start:
            return self.number(inputs, range_start)
        if range_start < 0:
            range_start = 1
        if range_end > len(inputs):
            range_end = len(inputs)
        newlist = []
        for i in range(range_start, range_end + 1):
            newlist.append(str(self.number(inputs, i)))
        return ' '.join(newlist)

    # split list by string
    def split(self, inputs, splitby):
        split_list = []
        restring = ' '.join(inputs)
        if splitby not in inputs:
            split_list = [restring]
        else:
            split_list = restring.split(splitby)
        return ' '.join(split_list)

    # exclude number
    def exclude(self, inputs, excludenum):
        try:
            del inputs[int(excludenum) - 1]
            return ' '.join(inputs)
        except IndexError:
            return ' '.join(inputs)

    # Forward Range includes index number
    def incrange_plus(self, inputs, range_start):
        return self.rangebetween(inputs, int(range_start), len(inputs))

    # Reverse Range includes index number
    def incrange_minus(self, inputs, range_end):
        return self.rangebetween(inputs, 1, int(range_end))

    # Forward Range excludes index number
    def excrange_plus(self, inputs, range_start):
        return self.rangebetween(inputs, int(range_start) + 1, len(inputs))

    # Reverse Range excludes index number
    def excrange_minus(self, inputs, range_end):
        return self.rangebetween(inputs, 1, int(range_end) - 1)

    # dedupe list
    def dedupe(self, inputs):
        newlist = []
        for inputspart in inputs:
            if inputspart not in newlist:
                newlist.append(inputspart)
        return newlist

    # Sort list
    def sort(self, inputs):
        return sorted(inputs)

    # reverse sort list
    def rsort(self, inputs):
        return sorted(inputs)[::-1]

    # count items in list, return dictionary
    def count(self, inputs):
        returndict = dict()
        uniqueinputitems, uniquecount = [], []
        for inputspart in inputs:
            if inputspart not in uniqueinputitems:
                uniqueinputitems.append(inputspart)
        for uniqueinputspart in uniqueinputitems:
            count = 0
            for ele in inputs:
                if (ele == uniqueinputspart):
                    count += 1
            uniquecount.append(count)
        for inputsitem, unumber in zip(uniqueinputitems, uniquecount):
            returndict[inputsitem] = unumber
        return returndict

    # random item from list
    def random(self, inputs):
        randomselectlist = list(inputs)
        while len(randomselectlist) > 1:
            random.shuffle(randomselectlist)
            randomselect = randomselectlist[random.randint(
                0,
                len(randomselectlist) - 1)]
            randomselectlist.remove(randomselect)
        randomselect = randomselectlist[0]
        return randomselect

    # remove random item from list
    def exrandom(self, inputs):
        randremove = self.random(inputs)
        inputs.remove(randremove)
        return inputs

    # Convert list into lowercase
    def lower(self, inputs):
        return [inputspart.lower() for inputspart in inputs]

    # Convert list to uppercase
    def upper(self, inputs):
        return [inputspart.upper() for inputspart in inputs]

    # Convert list to uppercase
    def title(self, inputs):
        return [inputspart.title() for inputspart in inputs]

    # Reverse List Order
    def reverse(self, inputs):
        return inputs[::-1]

    def list_nospace(self, inputs):
        return ','.join(str(x) for x in inputs)

    # comma seperated list with and
    def andlist(self, inputs):
        if len(inputs) < 2:
            return ' '.join(inputs)
        lastentry = str("and " + str(inputs[len(inputs) - 1]))
        del inputs[-1]
        inputs.append(lastentry)
        if len(inputs) == 2:
            return ' '.join(inputs)
        return ', '.join(str(x) for x in inputs)

    # comma seperated list with or
    def orlist(self, inputs):
        if len(inputs) < 2:
            return ' '.join(inputs)
        lastentry = str("or " + str(inputs[len(inputs) - 1]))
        del inputs[-1]
        inputs.append(lastentry)
        if len(inputs) == 2:
            return ' '.join(inputs)
        return ', '.join(str(x) for x in inputs)


spicemanip = Spicemanip()
