# main.py
"""This is main class for running the roku language compiler.

- TODO

"""
import sys
import os
import click

from compiler.lexical_analyser import LexicalAnalyser
from compiler.syntax_analyser import SyntaxAnalyser

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
	syntax = SyntaxAnalyser()

	print('Loading syntax rules...')
	syntax.load_rules(syntax_rules_path)
		
	print('Generating syntax tree...')
	tree = syntax.create_tree(tuples)

	print_tuples(tuples)
	print_node(tree, 0)

	print(f'result: {str(tree.length())}')
	print(f'expected: {str(len(tuples))}')


def print_node(node, level):
	string = ''
	for i in range(0, level):
		if i == level-1:
			string += '╚══ '
		else:
			string += '    '
		
	if isinstance(node.core, tuple):
		string += node.core[1]
	else:
		string += node.core

	print(string)

	for child in node.children:
		print_node(child, level+1)


def print_tuples(tuples):
	for i, element in enumerate(tuples):
		if len(element) == 3:
			print(str(i) + ' token: ' + element[1] + ' value: ' 
				+ element[2] + ' -> on line ' + str(element[0][1]) + 
				':' + str(element[0][0]))
		else:
			print(str(i) + ' token: ' + element[1] + ' -> on line ' +
				str(element[0][1]) + ':' + str(element[0][0]))


if __name__ == '__main__':
	main()
