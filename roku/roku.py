# main.py
"""This is main class for running the roku language compiler.

- TODO

"""
import sys
import os

from lexical.lexical_analyser import LexicalAnalyser

dir = os.path.dirname(__file__)
lexical_categories_path = os.path.join(dir, 'resources/lexical_categories.json')
syntax_rules_path = os.path.join(dir, 'resources/syntax_rules.json')


def main():

	if len(sys.argv) <= 1:
		print('Please provide an input file. Usage: python3 roku.py input.fang')
		return

	file = sys.argv[1]

	print('Creating analyser...')
	analyser = LexicalAnalyser()

	print('Loading categories...')
	analyser.load_categories(lexical_categories_path)

	print('Generating tuples...')
	tuples = analyser.parse_input(file)

	# just for dev
	for i, element in enumerate(tuples):
		if isinstance(element, tuple):
			print(str(i) + ' token: ' + element[0] + ' value: ' + element[1])
		else:
			print(str(i) + ' token: ' + element)
		

if __name__ == '__main__':
	main()
