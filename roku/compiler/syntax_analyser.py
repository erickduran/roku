# syntax_analyser.py
"""This is the syntax analyser for the roku programming language.

The main objective of this class is to read the tuples from the
lexical analyser and produce the abstract syntax tree (AST).
"""
import json

from entities import Node

class SyntaxAnalyser:
	def __init__(self):
		self.__tuples = []
		self.__length = None
		self.__rules = []
		self.__last_correct_tuple = None
		
	def create_tree(self, tuples):
		self.__tuples = tuples
		self.__length = len(tuples)

		tree, result = self.check(':s', 0)

		# just for dev
		print('result: ' + str(result))
		print('expected: ' + str(self.__length))

		if tree is None:
			message = f'syntax error on line {self.__last_correct_tuple[0][1]}:{self.__last_correct_tuple[0][0]}'
			raise SyntaxError(message)

		return tree

	def load_rules(self, path):
		file = open(path, 'r')
		self.__rules = json.load(file)
		
	def check(self, rule, i):
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

		for option in rule['rule_options']:
			result_index = i
			for rule in option:
				child, result_index = self.check(rule, result_index)

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
