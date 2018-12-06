# main.py
"""This is main class for running the roku language compiler.

The main objective of this class is to read the input source file 
and produce the final tuples from the lexical, syntax and semantic
analysers.

"""
import sys
import os
import click

from compiler.lexical_analyser import LexicalAnalyser
from compiler.syntax_analyser import SyntaxAnalyser
from compiler.semantic_analyser import SemanticAnalyser
from tree import Tree

dir = os.path.dirname(__file__)
lexical_categories_path = os.path.join(dir, 
	'resources/lexical_categories.json')
syntax_rules_path = os.path.join(dir, 
	'resources/syntax_rules.json')
semantic_rules_path = os.path.join(dir, 
	'resources/semantic_rules.json')

@click.command()
@click.argument('source_file')
@click.option('--output_file', '-o', help='Name of the output file.')
@click.option('--verbose', '-v', is_flag=True, help='Print log of each step.')
@click.option('--tuples', '-t', is_flag=True, help='Print the tuples generated by the lexical analyser.')
@click.option('--ast', '-a', is_flag=True, help='Print the generated abstract syntax tree.')
@click.option('--decorated', '-d', is_flag=True, help='Print the generated abstract syntax tree with type decorations.')
@click.option('--bonus', '-b', is_flag=True, help='Bonus option.')
def main(source_file, output_file, verbose, tuples, ast, decorated, bonus):
	file = source_file

	if verbose:
		print('Creating lexical analyser...')
	analyser = LexicalAnalyser()

	if verbose:
		print('Loading categories...')
	analyser.load_categories(lexical_categories_path)

	if verbose:
		print('Generating tuples...')
	parsed_tuples = analyser.parse_input(file)

	if verbose:
		print('Creating syntax analyser...')
	syntax = SyntaxAnalyser()

	if verbose:
		print('Loading syntax rules...')
	syntax.load_rules(syntax_rules_path)
		
	if verbose:
		print('Generating syntax tree...')
	tree = syntax.create_tree(parsed_tuples)

	if verbose:
		print('Creating semantic analyser...')
	semantic = SemanticAnalyser()

	if verbose:
		print('Loading semantic rules...')
	semantic.load_rules(semantic_rules_path)

	if verbose:
		print('Decorating syntax tree...')
	semantic.check_type(tree)

	if tuples:
		print_tuples(parsed_tuples)

	if ast:
		print_node(tree, 0)

	if decorated:
		print_node(tree, 0, True)

	if bonus:
		tree = Tree()
		print(tree.tree)


def print_node(node, level, decorated=False):
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

	if decorated:
		if node.type is not None:
			string += ' (' + node.type + ')'

	if decorated:
		if node.rule is not None:
			string += ' [by rule option: ' + str(node.rule) + ']'

	print(string)

	for child in node.children:
		print_node(child, level+1, decorated)


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
