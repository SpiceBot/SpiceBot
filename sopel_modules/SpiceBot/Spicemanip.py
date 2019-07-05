#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Top-level package for spicemanip."""

__author__ = """Sam Zick"""
__email__ = 'sam@deathbybandaid.net'
__version__ = '0.1.7'

# import random
import collections


class spicemanipnew():

    def __init__(self, inputs, output_type=None):

        self.inputs = inputs
        self.inputs_list = self.input_handler(self.inputs)
        return self.inputs_list

    def input_handler(self, inputs):
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
        return inputs

    def output_handler(self, outputs, output_type=None):
        if not output_type:
            output_type = "list"
        return outputs

    def core(self, inputs=None, task='create', output_type=None):
        if not inputs:
            return self.output_handler([""], output_type=None)

    """
    # Hub
    def main(self, inputs, outputtask, output_type='default'):

        # TODO 'this*that' or '1*that' replace either all strings matching, or an index value
        # TODO reverse sort z.sort(reverse = True)
        # list.extend adds lists to eachother

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
            returnvalue = eval('spicemanip_' + outputtask + '(inputs, outputtask, mainoutputtask, suboutputtask)')

        # default return if not specified
        if output_type == 'default':
            if outputtask in [
                                'string', 'number', 'rangebetween', 'exclude', 'random',
                                'incrange_plus', 'incrange_minus', 'excrange_plus', 'excrange_minus'
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
    def spicemanip_index(self, indexitem, outputtask, arraytoindex, arraytocompare):
        item = ''
        for x, y in zip(arraytoindex, arraytocompare):
            if x == indexitem:
                item = y
        return item

    # split list by string
    def spicemanip_split(self, inputs, outputtask, mainoutputtask, suboutputtask):
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
    def spicemanip_dedupe(self, inputs, outputtask, mainoutputtask, suboutputtask):
        newlist = []
        for inputspart in inputs:
            if inputspart not in newlist:
                newlist.append(inputspart)
        return newlist

    # Sort list
    def spicemanip_sort(self, inputs, outputtask, mainoutputtask, suboutputtask):
        return sorted(inputs)

    # reverse sort list
    def spicemanip_rsort(self, inputs, outputtask, mainoutputtask, suboutputtask):
        return sorted(inputs)[::-1]

    # count items in list, return dictionary
    def spicemanip_count(self, inputs, outputtask, mainoutputtask, suboutputtask):
        returndict = dict()
        if inputs == []:
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
    def spicemanip_random(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        randomselectlist = []
        for temppart in inputs:
            randomselectlist.append(temppart)
        while len(randomselectlist) > 1:
            random.shuffle(randomselectlist)
            randomselect = randomselectlist[random.randint(0, len(randomselectlist) - 1)]
            randomselectlist.remove(randomselect)
        randomselect = randomselectlist[0]
        return randomselect

    # remove random item from list
    def spicemanip_exrandom(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return []
        randremove = self.spicemanip_random(inputs, outputtask, mainoutputtask, suboutputtask)
        inputs.remove(randremove)
        return inputs

    # Convert list into lowercase
    def spicemanip_lower(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return [inputspart.lower() for inputspart in inputs]

    # Convert list to uppercase
    def spicemanip_upper(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return [inputspart.upper() for inputspart in inputs]

    # Convert list to uppercase
    def spicemanip_title(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return [inputspart.title() for inputspart in inputs]

    # Reverse List Order
    def spicemanip_reverse(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return []
        return inputs[::-1]

    # comma seperated list
    def spicemanip_list(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return ', '.join(str(x) for x in inputs)

    def spicemanip_list_nospace(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return ','.join(str(x) for x in inputs)

    # comma seperated list with and
    def spicemanip_andlist(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
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
    def spicemanip_orlist(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
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
    def spicemanip_exclude(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        del inputs[int(mainoutputtask) - 1]
        return ' '.join(inputs)

    # Convert list to string
    def spicemanip_string(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return ' '.join(inputs)

    # Get number item from list
    def spicemanip_number(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        elif len(inputs) == 1:
            return inputs[0]
        elif int(mainoutputtask) > len(inputs) or int(mainoutputtask) < 0:
            return ''
        else:
            return inputs[int(mainoutputtask) - 1]

    # Get Last item from list
    def spicemanip_last(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return inputs[len(inputs) - 1]

    # range between items in list
    def spicemanip_rangebetween(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        if not str(mainoutputtask).isdigit() or not str(suboutputtask).isdigit():
            return ''
        mainoutputtask, suboutputtask = int(mainoutputtask), int(suboutputtask)
        if suboutputtask == mainoutputtask:
            return self.spicemanip_number(inputs, outputtask, mainoutputtask, suboutputtask)
        if suboutputtask < mainoutputtask:
            return []
        if mainoutputtask < 0:
            mainoutputtask = 1
        if suboutputtask > len(inputs):
            suboutputtask = len(inputs)
        newlist = []
        for i in range(mainoutputtask, suboutputtask + 1):
            newlist.append(str(self.spicemanip_number(inputs, outputtask, i, suboutputtask)))
        if newlist == []:
            return ''
        return ' '.join(newlist)

    # Forward Range includes index number
    def spicemanip_incrange_plus(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask, int(mainoutputtask), len(inputs))

    # Reverse Range includes index number
    def spicemanip_incrange_minus(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask, 1, int(mainoutputtask))

    # Forward Range excludes index number
    def spicemanip_excrange_plus(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask, int(mainoutputtask) + 1, len(inputs))

    # Reverse Range excludes index number
    def spicemanip_excrange_minus(self, inputs, outputtask, mainoutputtask, suboutputtask):
        if inputs == []:
            return ''
        return self.spicemanip_rangebetween(inputs, outputtask, 1, int(mainoutputtask) - 1)
"""
