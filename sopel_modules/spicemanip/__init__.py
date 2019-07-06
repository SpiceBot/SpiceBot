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

"""
class Spicemanip_new():
    def __init__(self):
        pass

    def __call__(self, inputs, task, output_type='default'):

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
        if not self.inputs or not len(self.inputs):
            self.input_list = []
            return
        if isinstance(self.inputs, list):
            self.input_list = self.inputs.copy()
            return
        if isinstance(self.inputs, collections.abc.KeysView):
            self.input_list = list(self.inputs)
            return
        if isinstance(self.inputs, dict):
            self.input_list = list(self.inputs.keys())
            return
        if not isinstance(self.inputs, list):
            self.input_list = self.inputs.split(" ")
            return

    def core_task_handler(self):

        # Create return
        if self.task in ['create']:
            self.outputs = self.input_list
            return

        if not len(self.input_list):
            self.outputs = []
            return

        if self.task in ["0", 0, 'complete']:
            self.outputs = self.string(self.input_list)
            self.task = "complete"

        elif self.task in ['index']:
            self.outputs = self.index(self.input_list[0], self.input_list[1],
                                      self.input_list[2])
            self.task = "index"

        elif self.task in ['last', '-1', -1]:
            self.outputs = self.last(self.input_list)
            self.task = "last"

        elif self.is_digit(self.task):
            self.outputs = self.number(self.input_list, int(self.task))
            self.task = "number"

        elif "^" in str(self.task):
            range_nums = str(self.task).split("^", 1).sort()
            range_start, range_end = range_nums[0], range_nums[1]
            self.outputs = self.rangebetween(self.input_list, int(range_start),
                                             int(range_end))
            self.task = "rangebetween"

        elif str(self.task).startswith("split_"):
            split_mark = str(self.task).replace("split_", "")
            self.outputs = self.split(self.input_list, split_mark)
            self.task = "split"

        elif str(self.task).endswith("!"):
            exclude_num = str(self.task).replace("!", "")
            self.outputs = self.exclude(self.input_list, int(exclude_num))
            self.task = "exclude"

        elif str(self.task).endswith("+"):
            range_start = str(self.task).replace("+", "")
            self.outputs = self.incrange_plus(self.input_list,
                                              int(range_start))
            self.task = "incrange_plus"

        elif str(self.task).endswith("-"):
            range_end = str(self.task).replace("-", "")
            self.outputs = self.incrange_minus(self.input_list, int(range_end))
            self.task = "incrange_minus"

        elif str(self.task).endswith(">"):
            range_start = str(self.task).replace(">", "")
            self.outputs = self.excrange_plus(self.input_list,
                                              int(range_start))
            self.task = "excrange_plus"

        elif str(self.task).endswith("<"):
            range_end = str(self.task).replace("<", "")
            self.outputs = self.excrange_minus(self.input_list, int(range_end))
            self.task = "excrange_minus"

        elif hasattr(self, str(
                self.task)) and not str(self.task).startswith("core_"):
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
            'count': "dict",
            "create": "list",
            'complete': "string",
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
    def complete(self, inputs):
        return self.string(inputs)

    def last(self, inputs):
        return self.number(inputs, -1)

    # Convert list to string
    def string(self, inputs):
        if not isinstance(inputs, list):
            return inputs
        if not inputs or not len(inputs):
            return ''
        return ' '.join(inputs)

    def create(self, inputs):
        return self.list(inputs)

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

    def is_digit(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False
"""


class Spicemanip():

    def __init__(self):
        pass

    def __call__(self, inputs, outputtask, output_type='default'):
        mainoutputtask, suboutputtask = None, None

        # Input needs to be a list, but don't split a word into letters
        if not inputs:
            inputs = []
        if isinstance(inputs, collections.abc.KeysView):
            inputs = list(inputs)
        elif isinstance(inputs, dict):
            inputs = list(inputs.keys())
        if not isinstance(inputs, list):
            inputs = list(inputs.split(" "))
            inputs = [x for x in inputs if x and x not in ['', ' ']]
            inputs = [inputspart.strip() for inputspart in inputs]

        # Create return
        if outputtask == 'create':
            return inputs

        # Make temparray to preserve original order
        temparray = []
        for inputpart in inputs:
            temparray.append(inputpart)
        inputs = temparray

        # Convert outputtask to standard
        if outputtask in [0, 'complete']:
            outputtask = 'string'
        elif outputtask == 'index':
            mainoutputtask = inputs[1]
            suboutputtask = inputs[2]
            inputs = inputs[0]
        elif str(outputtask).isdigit():
            mainoutputtask, outputtask = int(outputtask), 'number'
        elif "^" in str(outputtask):
            mainoutputtask = str(outputtask).split("^", 1)[0]
            suboutputtask = str(outputtask).split("^", 1)[1]
            outputtask = 'rangebetween'
            if int(suboutputtask) < int(mainoutputtask):
                mainoutputtask, suboutputtask = suboutputtask, mainoutputtask
        elif str(outputtask).startswith("split_"):
            mainoutputtask = str(outputtask).replace("split_", "")
            outputtask = 'split'
        elif str(outputtask).endswith(tuple(["!", "+", "-", "<", ">"])):
            mainoutputtask = str(outputtask)
            if str(outputtask).endswith("!"):
                outputtask = 'exclude'
            if str(outputtask).endswith("+"):
                outputtask = 'incrange_plus'
            if str(outputtask).endswith("-"):
                outputtask = 'incrange_minus'
            if str(outputtask).endswith(">"):
                outputtask = 'excrange_plus'
            if str(outputtask).endswith("<"):
                outputtask = 'excrange_minus'
            for r in (("!", ""), ("+", ""), ("-", ""), ("<", ""), (">", "")):
                mainoutputtask = mainoutputtask.replace(*r)
        if mainoutputtask == 'last':
            mainoutputtask = len(inputs)

        if outputtask == 'string':
            returnvalue = inputs
        else:
            returnvalue = eval(
                'spicemanip_' + outputtask +
                '(inputs, outputtask, mainoutputtask, suboutputtask)')

        # default return if not specified
        if output_type == 'default':
            if outputtask in [
                    'string', 'number', 'rangebetween', 'exclude', 'random',
                    'incrange_plus', 'incrange_minus', 'excrange_plus',
                    'excrange_minus'
            ]:
                output_type = 'string'
            elif outputtask in ['count']:
                output_type = 'dict'

        # verify output is correct
        if output_type == 'return':
            return returnvalue
        if output_type == 'string':
            if isinstance(returnvalue, list):
                returnvalue = ' '.join(returnvalue)
        elif output_type in ['list', 'array']:
            if not isinstance(returnvalue, list):
                returnvalue = list(returnvalue.split(" "))
                returnvalue = [
                    x for x in returnvalue if x and x not in ['', ' ']
                ]
                returnvalue = [
                    inputspart.strip() for inputspart in returnvalue
                ]
        return returnvalue

    # compare 2 lists, based on the location of an index item, passthrough needs to be [indexitem, arraytoindex, arraytocompare]
    def spicemanip_index(self, indexitem, outputtask, arraytoindex,
                         arraytocompare):
        item = ''
        for x, y in zip(arraytoindex, arraytocompare):
            if x == indexitem:
                item = y
        return item

    # split list by string
    def spicemanip_split(self, inputs, outputtask, mainoutputtask,
                         suboutputtask):
        split_array = []
        restring = ' '.join(inputs)
        if mainoutputtask not in inputs:
            split_array = [restring]
        else:
            split_array = restring.split(mainoutputtask)
        split_array = [x for x in split_array if x and x not in ['', ' ']]
        split_array = [inputspart.strip() for inputspart in split_array]
        if split_array == []:
            split_array = [[]]
        return split_array

    # dedupe list
    def spicemanip_dedupe(self, inputs, outputtask, mainoutputtask,
                          suboutputtask):
        newlist = []
        for inputspart in inputs:
            if inputspart not in newlist:
                newlist.append(inputspart)
        return newlist

    # Sort list
    def spicemanip_sort(self, inputs, outputtask, mainoutputtask,
                        suboutputtask):
        return sorted(inputs)

    # reverse sort list
    def spicemanip_rsort(self, inputs, outputtask, mainoutputtask,
                         suboutputtask):
        return sorted(inputs)[::-1]

    # count items in list, return dictionary
    def spicemanip_count(self, inputs, outputtask, mainoutputtask,
                         suboutputtask):
        returndict = dict()
        if not len(inputs):
            return returndict
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
    def spicemanip_random(self, inputs, outputtask, mainoutputtask,
                          suboutputtask):
        if not len(inputs):
            return ''
        randomselectlist = []
        for temppart in inputs:
            randomselectlist.append(temppart)
        while len(randomselectlist) > 1:
            random.shuffle(randomselectlist)
            randomselect = randomselectlist[random.randint(
                0,
                len(randomselectlist) - 1)]
            randomselectlist.remove(randomselect)
        randomselect = randomselectlist[0]
        return randomselect

    # remove random item from list
    def spicemanip_exrandom(self, inputs, outputtask, mainoutputtask,
                            suboutputtask):
        if not len(inputs):
            return []
        randremove = self.spicemanip_random(inputs, outputtask, mainoutputtask,
                                            suboutputtask)
        inputs.remove(randremove)
        return inputs

    # Convert list into lowercase
    def spicemanip_lower(self, inputs, outputtask, mainoutputtask,
                         suboutputtask):
        if not len(inputs):
            return ''
        return [inputspart.lower() for inputspart in inputs]

    # Convert list to uppercase
    def spicemanip_upper(self, inputs, outputtask, mainoutputtask,
                         suboutputtask):
        if not len(inputs):
            return ''
        return [inputspart.upper() for inputspart in inputs]

    # Convert list to uppercase
    def spicemanip_title(self, inputs, outputtask, mainoutputtask,
                         suboutputtask):
        if not len(inputs):
            return ''
        return [inputspart.title() for inputspart in inputs]

    # Reverse List Order
    def spicemanip_reverse(self, inputs, outputtask, mainoutputtask,
                           suboutputtask):
        if not len(inputs):
            return []
        return inputs[::-1]

    # comma seperated list
    def spicemanip_list(self, inputs, outputtask, mainoutputtask,
                        suboutputtask):
        if not len(inputs):
            return ''
        return ', '.join(str(x) for x in inputs)

    def spicemanip_list_nospace(self, inputs, outputtask, mainoutputtask,
                                suboutputtask):
        if not len(inputs):
            return ''
        return ','.join(str(x) for x in inputs)

    # comma seperated list with and
    def spicemanip_andlist(self, inputs, outputtask, mainoutputtask,
                           suboutputtask):
        if not len(inputs):
            return ''
        if len(inputs) < 2:
            return ' '.join(inputs)
        lastentry = str("and " + str(inputs[len(inputs) - 1]))
        del inputs[-1]
        inputs.append(lastentry)
        if len(inputs) == 2:
            return ' '.join(inputs)
        return ', '.join(str(x) for x in inputs)

    # comma seperated list with or
    def spicemanip_orlist(self, inputs, outputtask, mainoutputtask,
                          suboutputtask):
        if not len(inputs):
            return ''
        if len(inputs) < 2:
            return ' '.join(inputs)
        lastentry = str("or " + str(inputs[len(inputs) - 1]))
        del inputs[-1]
        inputs.append(lastentry)
        if len(inputs) == 2:
            return ' '.join(inputs)
        return ', '.join(str(x) for x in inputs)

    # exclude number
    def spicemanip_exclude(self, inputs, outputtask, mainoutputtask,
                           suboutputtask):
        if not len(inputs):
            return ''
        del inputs[int(mainoutputtask) - 1]
        return ' '.join(inputs)

    # Convert list to string
    def spicemanip_string(self, inputs, outputtask, mainoutputtask,
                          suboutputtask):
        if not len(inputs):
            return ''
        return ' '.join(inputs)

    # Get number item from list
    def spicemanip_number(self, inputs, outputtask, mainoutputtask,
                          suboutputtask):
        if not len(inputs):
            return ''
        elif len(inputs) == 1:
            return inputs[0]
        elif int(mainoutputtask) > len(inputs) or int(mainoutputtask) < 0:
            return ''
        else:
            return inputs[int(mainoutputtask) - 1]

    # Get Last item from list
    def spicemanip_last(self, inputs, outputtask, mainoutputtask,
                        suboutputtask):
        if not len(inputs):
            return ''
        return inputs[len(inputs) - 1]

    # range between items in list
    def spicemanip_rangebetween(self, inputs, outputtask, mainoutputtask,
                                suboutputtask):
        if not len(inputs):
            return ''
        if not str(mainoutputtask).isdigit() or not str(
                suboutputtask).isdigit():
            return ''
        mainoutputtask, suboutputtask = int(mainoutputtask), int(suboutputtask)
        if suboutputtask == mainoutputtask:
            return self.spicemanip_number(inputs, outputtask, mainoutputtask,
                                          suboutputtask)
        if suboutputtask < mainoutputtask:
            return []
        if mainoutputtask < 0:
            mainoutputtask = 1
        if suboutputtask > len(inputs):
            suboutputtask = len(inputs)
        newlist = []
        for i in range(mainoutputtask, suboutputtask + 1):
            newlist.append(
                str(
                    self.spicemanip_number(inputs, outputtask, i,
                                           suboutputtask)))
        if newlist == []:
            return ''
        return ' '.join(newlist)

    # Forward Range includes index number
    def spicemanip_incrange_plus(self, inputs, outputtask, mainoutputtask,
                                 suboutputtask):
        if not len(inputs):
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask,
                                            int(mainoutputtask), len(inputs))

    # Reverse Range includes index number
    def spicemanip_incrange_minus(self, inputs, outputtask, mainoutputtask,
                                  suboutputtask):
        if not len(inputs):
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask, 1,
                                            int(mainoutputtask))

    # Forward Range excludes index number
    def spicemanip_excrange_plus(self, inputs, outputtask, mainoutputtask,
                                 suboutputtask):
        if not len(inputs):
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask,
                                            int(mainoutputtask) + 1,
                                            len(inputs))

    # Reverse Range excludes index number
    def spicemanip_excrange_minus(self, inputs, outputtask, mainoutputtask,
                                  suboutputtask):
        if not len(inputs):
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask, 1,
                                            int(mainoutputtask) - 1)


spicemanip = Spicemanip()

"""
# Hub
def spicemanip(inputs, outputtask, output_type='default'):

    mainoutputtask, suboutputtask = None, None

    # Input needs to be a list, but don't split a word into letters
    if not inputs:
        inputs = []
    if isinstance(inputs, collections.abc.KeysView):
        inputs = list(inputs)
    elif isinstance(inputs, dict):
        inputs = list(inputs.keys())
    if not isinstance(inputs, list):
        inputs = list(inputs.split(" "))
        inputs = [x for x in inputs if x and x not in ['', ' ']]
        inputs = [inputspart.strip() for inputspart in inputs]

    # Create return
    if outputtask == 'create':
        return inputs

    # Make temparray to preserve original order
    temparray = []
    for inputpart in inputs:
        temparray.append(inputpart)
    inputs = temparray

    # Convert outputtask to standard
    if outputtask in [0, 'complete']:
        outputtask = 'string'
    elif outputtask == 'index':
        mainoutputtask = inputs[1]
        suboutputtask = inputs[2]
        inputs = inputs[0]
    elif str(outputtask).isdigit():
        mainoutputtask, outputtask = int(outputtask), 'number'
    elif "^" in str(outputtask):
        mainoutputtask = str(outputtask).split("^", 1)[0]
        suboutputtask = str(outputtask).split("^", 1)[1]
        outputtask = 'rangebetween'
        if int(suboutputtask) < int(mainoutputtask):
            mainoutputtask, suboutputtask = suboutputtask, mainoutputtask
    elif str(outputtask).startswith("split_"):
        mainoutputtask = str(outputtask).replace("split_", "")
        outputtask = 'split'
    elif str(outputtask).endswith(tuple(["!", "+", "-", "<", ">"])):
        mainoutputtask = str(outputtask)
        if str(outputtask).endswith("!"):
            outputtask = 'exclude'
        if str(outputtask).endswith("+"):
            outputtask = 'incrange_plus'
        if str(outputtask).endswith("-"):
            outputtask = 'incrange_minus'
        if str(outputtask).endswith(">"):
            outputtask = 'excrange_plus'
        if str(outputtask).endswith("<"):
            outputtask = 'excrange_minus'
        for r in (("!", ""), ("+", ""), ("-", ""), ("<", ""), (">", "")):
            mainoutputtask = mainoutputtask.replace(*r)
    if mainoutputtask == 'last':
        mainoutputtask = len(inputs)

    if outputtask == 'string':
        returnvalue = inputs
    else:
        returnvalue = eval(
            'spicemanip_' + outputtask +
            '(inputs, outputtask, mainoutputtask, suboutputtask)')

    # default return if not specified
    if output_type == 'default':
        if outputtask in [
                'string', 'number', 'rangebetween', 'exclude', 'random',
                'incrange_plus', 'incrange_minus', 'excrange_plus',
                'excrange_minus'
        ]:
            output_type = 'string'
        elif outputtask in ['count']:
            output_type = 'dict'

    # verify output is correct
    if output_type == 'return':
        return returnvalue
    if output_type == 'string':
        if isinstance(returnvalue, list):
            returnvalue = ' '.join(returnvalue)
    elif output_type in ['list', 'array']:
        if not isinstance(returnvalue, list):
            returnvalue = list(returnvalue.split(" "))
            returnvalue = [x for x in returnvalue if x and x not in ['', ' ']]
            returnvalue = [inputspart.strip() for inputspart in returnvalue]
    return returnvalue


# compare 2 lists, based on the location of an index item, passthrough needs to be [indexitem, arraytoindex, arraytocompare]
def spicemanip_index(indexitem, outputtask, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item


# split list by string
def spicemanip_split(inputs, outputtask, mainoutputtask, suboutputtask):
    split_array = []
    restring = ' '.join(inputs)
    if mainoutputtask not in inputs:
        split_array = [restring]
    else:
        split_array = restring.split(mainoutputtask)
    split_array = [x for x in split_array if x and x not in ['', ' ']]
    split_array = [inputspart.strip() for inputspart in split_array]
    if split_array == []:
        split_array = [[]]
    return split_array


# dedupe list
def spicemanip_dedupe(inputs, outputtask, mainoutputtask, suboutputtask):
    newlist = []
    for inputspart in inputs:
        if inputspart not in newlist:
            newlist.append(inputspart)
    return newlist


# Sort list
def spicemanip_sort(inputs, outputtask, mainoutputtask, suboutputtask):
    return sorted(inputs)


# reverse sort list
def spicemanip_rsort(inputs, outputtask, mainoutputtask, suboutputtask):
    return sorted(inputs)[::-1]


# count items in list, return dictionary
def spicemanip_count(inputs, outputtask, mainoutputtask, suboutputtask):
    returndict = dict()
    if not len(inputs):
        return returndict
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
def spicemanip_random(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    randomselectlist = []
    for temppart in inputs:
        randomselectlist.append(temppart)
    while len(randomselectlist) > 1:
        random.shuffle(randomselectlist)
        randomselect = randomselectlist[random.randint(
            0,
            len(randomselectlist) - 1)]
        randomselectlist.remove(randomselect)
    randomselect = randomselectlist[0]
    return randomselect


# remove random item from list
def spicemanip_exrandom(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return []
    randremove = spicemanip_random(inputs, outputtask, mainoutputtask,
                                   suboutputtask)
    inputs.remove(randremove)
    return inputs


# Convert list into lowercase
def spicemanip_lower(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    return [inputspart.lower() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_upper(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    return [inputspart.upper() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_title(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    return [inputspart.title() for inputspart in inputs]


# Reverse List Order
def spicemanip_reverse(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return []
    return inputs[::-1]


# comma seperated list
def spicemanip_list(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    return ', '.join(str(x) for x in inputs)


def spicemanip_list_nospace(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    return ','.join(str(x) for x in inputs)


# comma seperated list with and
def spicemanip_andlist(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("and " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# comma seperated list with or
def spicemanip_orlist(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("or " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# exclude number
def spicemanip_exclude(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    del inputs[int(mainoutputtask) - 1]
    return ' '.join(inputs)


# Convert list to string
def spicemanip_string(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    return ' '.join(inputs)


# Get number item from list
def spicemanip_number(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    elif len(inputs) == 1:
        return inputs[0]
    elif int(mainoutputtask) > len(inputs) or int(mainoutputtask) < 0:
        return ''
    else:
        return inputs[int(mainoutputtask) - 1]


# Get Last item from list
def spicemanip_last(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    return inputs[len(inputs) - 1]


# range between items in list
def spicemanip_rangebetween(inputs, outputtask, mainoutputtask, suboutputtask):
    if not len(inputs):
        return ''
    if not str(mainoutputtask).isdigit() or not str(suboutputtask).isdigit():
        return ''
    mainoutputtask, suboutputtask = int(mainoutputtask), int(suboutputtask)
    if suboutputtask == mainoutputtask:
        return spicemanip_number(inputs, outputtask, mainoutputtask,
                                 suboutputtask)
    if suboutputtask < mainoutputtask:
        return []
    if mainoutputtask < 0:
        mainoutputtask = 1
    if suboutputtask > len(inputs):
        suboutputtask = len(inputs)
    newlist = []
    for i in range(mainoutputtask, suboutputtask + 1):
        newlist.append(
            str(spicemanip_number(inputs, outputtask, i, suboutputtask)))
    if newlist == []:
        return ''
    return ' '.join(newlist)


# Forward Range includes index number
def spicemanip_incrange_plus(inputs, outputtask, mainoutputtask,
                             suboutputtask):
    if not len(inputs):
        return ''
    return spicemanip_rangebetween(inputs, outputtask, int(mainoutputtask),
                                   len(inputs))


# Reverse Range includes index number
def spicemanip_incrange_minus(inputs, outputtask, mainoutputtask,
                              suboutputtask):
    if not len(inputs):
        return ''
    return spicemanip_rangebetween(inputs, outputtask, 1, int(mainoutputtask))


# Forward Range excludes index number
def spicemanip_excrange_plus(inputs, outputtask, mainoutputtask,
                             suboutputtask):
    if not len(inputs):
        return ''
    return spicemanip_rangebetween(inputs, outputtask,
                                   int(mainoutputtask) + 1, len(inputs))


# Reverse Range excludes index number
def spicemanip_excrange_minus(inputs, outputtask, mainoutputtask,
                              suboutputtask):
    if not len(inputs):
        return ''
    return spicemanip_rangebetween(inputs, outputtask, 1,
                                   int(mainoutputtask) - 1)
"""
