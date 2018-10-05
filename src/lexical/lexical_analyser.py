# lexical_analyser.py
"""This is the lexical analyser for the roku programming language.

The main objective of this class is to read the input source file 
and produce the tuples of the lexical analysis. The symbol table 
entries will be embedded in the tuples.
"""

import json
import re

from lexical.lexical_errors import *


class LexicalAnalyser:
    def __init__(self):
        self.__tuples = []
        self.__categories = []

    def load_categories(self, path):
        """Takes the path of the 
        """
        file = open(path, 'r')
        self.__categories = json.load(file)
        pass

    def parse_input(self, source_code):
        self.__tuples = []
        file = open(source_code, 'r').read()

        current_string = ''
        last_correct_string = ''
        last_correct_category = None

        i = 0
        line_number = 1
        file_length = len(file)

        def add_to_tuples(category, string):
            if category['is_unique']:
                self.__add_tuple(token=category['token'])
            else:
                self.__add_tuple(token=category['token'], value=string)

        def reset_all_current_values():
            nonlocal current_string
            nonlocal last_correct_string
            nonlocal last_correct_category

            current_string = ''
            last_correct_string = ''
            last_correct_category = None
        
        while i < file_length:
            char = file[i]
            current_string += char

            found_category = self.__check_symbol(current_string)
            if found_category is not None:
                last_correct_string = current_string
                last_correct_category = found_category
                i += 1

                if i == file_length:
                    add_to_tuples(found_category, current_string)
            else:
                if last_correct_category is not None:
                    add_to_tuples(last_correct_category, last_correct_string)
                    reset_all_current_values()
                else:
                    is_space = False
                    match_result = re.match(self.__categories['spaces']['regex'], current_string)

                    if match_result is not None:
                        if match_result.start() == 0 and match_result.end() == len(current_string):
                            if current_string == '\n':
                                line_number += 1
                            is_space = True

                    if not is_space:
                        message = 'lex error in line %d: character not identified: \'%s\'' % (line_number, current_string)
                        raise InvalidCharacterError(message)

                    reset_all_current_values()
                    i += 1

        return self.__tuples

    def __add_tuple(self, token, value=None):
        if value:
            self.__tuples.append((token, value))
        else:
            self.__tuples.append(token)

    def __check_symbol(self, symbol):
        for category in self.__categories['categories']:
            match_result = re.match(category['regex'], symbol)

            if match_result is not None:
                if match_result.start() == 0 and match_result.end() == len(symbol):
                    if 'action' in category:
                        if category['action'] == 'check_value':
                            is_word_result = self.__check_in_words(symbol)
                            if is_word_result is not None:
                                return is_word_result
                            else:
                                return category
                    else:
                        return category
        return None

    def __check_in_words(self, symbol):
        for word in self.__categories['language_words']:
            match_result = re.match(word['regex'], symbol)
            if match_result is not None:
                if match_result.start() == 0 and match_result.end() == len(symbol):
                    return word
        return None
