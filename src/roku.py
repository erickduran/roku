# main.py
"""This is main class for running the roku language compiler.

- TODO

"""
import sys

from lexical.lexical_analyser import LexicalAnalyser


def main():

	if len(sys.argv) <= 1:
		print('Please provide an input file. Usage: python3 roku.py input.fang')
		return

	file = sys.argv[1]

	print('Creating analyser...')
	analyser = LexicalAnalyser()

	print('Loading categories...')
	analyser.load_categories('lexical/lexical_categories.json')

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
