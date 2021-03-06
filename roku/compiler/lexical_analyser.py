# lexical_analyser.py
"""This is the lexical analyser for the roku programming language.

The main objective of this class is to read the input source file 
and produce the tuples of the lexical analysis. The symbol table 
entries will be embedded in the tuples.
"""

import json
import re
import collections

from errors import InvalidCharacterError, EmptyFileError


class LexicalAnalyser:

    def __init__(self):
        self.__tuples = []
        self.__categories = []
        self.Char = collections.namedtuple('Char', ('value', 
            'char_num', 'line_num'))


    def load_categories(self, path):
        """Takes the path of the categories definition file and loads 
        them to a local dictionary.
        """
        file = open(path, 'r')
        self.__categories = json.load(file)


    def parse_input(self, source_code_path):
        self.__tuples = []
        file = self.__file_generator(source_code_path)

        current_string = ''
        last_correct_string = ''
        last_correct_category = None
        first_char_of_tuple = None

        def add_to_tuples(category, string, first_char_of_tuple):
            if category['is_unique']:
                self.__add_tuple(token=category['token'], 
                    location=(first_char_of_tuple.char_num, 
                        first_char_of_tuple.line_num))
            else:
                self.__add_tuple(token=category['token'],  
                    location=(first_char_of_tuple.char_num, 
                        first_char_of_tuple.line_num), value=string)

        def reset_all_current_values():
            nonlocal current_string
            nonlocal last_correct_string
            nonlocal last_correct_category
            nonlocal first_char_of_tuple

            current_string = ''
            last_correct_string = ''
            last_correct_category = None
            first_char_of_tuple = None
        
        char = next(file, None)

        if char is None:
            raise EmptyFileError('The input file is empty.')

        while char is not None:
            current_string += char.value

            if first_char_of_tuple is None:
                first_char_of_tuple = char

            found_category = self.__check_symbol(current_string)
            if found_category is not None:
                last_correct_string = current_string
                last_correct_category = found_category
                char = next(file, None)

                if char is None:
                    add_to_tuples(found_category, current_string,
                        first_char_of_tuple)
            else:
                if last_correct_category is not None:
                    add_to_tuples(last_correct_category, 
                        last_correct_string, first_char_of_tuple)
                    reset_all_current_values()
                else:
                    is_space = False
                    match_result = re.match(
                        self.__categories['spaces']['regex'], 
                        current_string)

                    if match_result is not None:
                        if match_result.start() == 0 and match_result.end() == len(current_string):
                            is_space = True

                    if not is_space:
                        message = f'lex error in line {char.line_num}:{char.char_num}: character not identified: \'{current_string}\''
                        raise InvalidCharacterError(message)

                    reset_all_current_values()
                    char = next(file, None)

        return self.__tuples


    def __file_generator(self, path):
        file = open(path, 'r')

        for line_num, line in enumerate(file):
            for char_num, char in enumerate(line):
                yield self.Char(char, char_num+1, line_num+1)


    def __add_tuple(self, token, location, value=None):
        if value:
            self.__tuples.append((location, token, value))
        else:
            self.__tuples.append((location, token))


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
        for word in self.__categories['reserved']:
            match_result = re.match(word['regex'], symbol)
            if match_result is not None:
                if match_result.start() == 0 and match_result.end() == len(symbol):
                    return word
        return None
        