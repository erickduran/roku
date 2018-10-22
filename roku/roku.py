# main.py
"""This is main class for running the roku language compiler.

- TODO

"""
import sys
import os
import click

from lexical.lexical_analyser import LexicalAnalyser
from syntax.syntax_analyser import SyntaxAnalyser

dir = os.path.dirname(__file__)
lexical_categories_path = os.path.join(dir, 
	'resources/lexical_categories.json')
syntax_rules_path = os.path.join(dir, 
	'resources/syntax_rules.json')

@click.command()
@click.argument('source_file')
@click.option('--output_file', '-o', help='Name of the output file.')
def main(source_file, output_file):
	file = source_file

	print('Creating lexical analyser...')
	analyser = LexicalAnalyser()

	print('Loading categories...')
	analyser.load_categories(lexical_categories_path)

	print('Generating tuples...')
	tuples = analyser.parse_input(file)

	print('Creating syntax analyser...')
	syntax = SyntaxAnalyser(tuples)

	print('Loading syntax rules...')
	syntax.load_rules(syntax_rules_path)
	
	# just for dev
	for i, element in enumerate(tuples):
		if len(element) == 3:
			print(str(i) + ' token: ' + element[1] + ' value: ' 
				+ element[2] + ' -> on line ' + str(element[0][1]) + 
				':' + str(element[0][0]))
		else:
			print(str(i) + ' token: ' + element[1] + ' -> on line ' +
				str(element[0][1]) + ':' + str(element[0][0]))
		
	print('Generating syntax tree...')
	syntax.start_analysis()

if __name__ == '__main__':
	main()
