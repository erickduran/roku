# syntax_analyser.py
"""This is the syntax analyser for the roku programming language.

The main objective of this class is to read the tuples from the
lexical analyser and produce the abstract syntax tree (AST).
"""
import json

from entities import Node
from errors import SyntaxError

class SyntaxAnalyser:

	def __init__(self):
		self.__tuples = []
		self.__rules = []
		self.__last_correct_tuple = None
		

	def create_tree(self, tuples):
		self.__tuples = tuples

		tree, result = self.__check(':s', 0)

		if tree is None or tree.length() != len(tuples):
			message = f'syntax error on line {self.__last_correct_tuple[0][1]}:{self.__last_correct_tuple[0][0]}'
			raise SyntaxError(message)

		return tree


	def load_rules(self, path):
		file = open(path, 'r')
		self.__rules = json.load(file)
		

	def __check(self, rule, i):
		if not rule.startswith(':'):
			if self.__tuples[i][1] == rule:
				return Node(self.__tuples[i]), i + 1
			else:
				self.__last_correct_tuple = self.__tuples[i]
				return None, None

		node = Node(rule)
		rule = self.__rules[rule]
		result_index = None

		max_node = None
		max_index = None

		for option_number, option in enumerate(rule['rule_options']):
			node.rule = option_number
			result_index = i
			for rule in option:
				child, result_index = self.__check(rule, result_index)

				if result_index is None:
					node.remove_children()
					break

				node.append(child)

			if node.children:
				if max_node is None or node.length() > max_node.length():
					max_node = node.copy()
					max_index = result_index
				node.remove_children()

		node = max_node
		result_index = max_index

		return node, result_index
