import json
import re


class LexicalAnalyser:
    def __init__(self):
        self.__symbol_table = []
        self.__categories = []

    def parse_input(self, source_code):
        file = open(source_code, 'r').read()

        current_string = ''
        last_correct_string = ''
        last_correct_category = ''

        i = 0
        file_length = len(file)

        while i < file_length:
            char = file[i]
            current_string += char
            # print('analysing: ' + self.current_string)

            found_category = self.check_symbol(current_string)
            if found_category is not None:
                last_correct_string = current_string
                last_correct_category = found_category
                i += 1

                if i == file_length:
                    # eof
                    print("'" + current_string + "'" + ' is ' + found_category['token'])
            else:
                if last_correct_category != '':
                    print("'" + last_correct_string + "'" + ' is ' + last_correct_category['token'])

                    current_string = ''
                    last_correct_string = ''
                    last_correct_category = ''
                else:
                    print("'" + current_string + "'" + ' was not found in categories')

                    current_string = ''
                    last_correct_string = ''
                    last_correct_category = ''
                    i += 1
        pass

    def add_to___symbol_table(self, token):
        pass

    def check_symbol(self, string):
        for category in self.__categories['categories']:
            match_result = re.match(category['regex'], string)

            if match_result is not None:
                if match_result.start() == 0 and match_result.end() == len(string):
                    if 'action' in category:
                        if category['action'] == 'check_value':
                            is_word_result = self.check_in_words(string)
                            if is_word_result is not None:
                                return is_word_result
                            else:
                                return category
                    else:
                        return category
        return None

    def check_in_words(self, string):
        for word in self.__categories['language_words']:
            if string == word['pattern']:
                return word
        return None

    def load_categories(self, path):
        file = open(path, 'r')
        self.__categories = json.load(file)
        pass
