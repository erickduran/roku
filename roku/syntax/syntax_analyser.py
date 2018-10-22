# syntax_analyser.py
"""This is the syntax analyser for the roku programming language.

The main objective of this class is to read the tuples from the
lexical analyser and produce the abstract syntax tree (AST).
"""
import json

class Node:
	def __init__(self, core):
		self.core = core
		self.children = []

	def append(self, node):
		self.children.append(node)

	def remove_children(self):
		self.children = []

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
		for option in rule['rule_options']:
			result_index = i
			for rule in option:
				child, result_index = self.check(rule, result_index)

				if result_index is None:
					node.remove_children()
					break

				node.append(child)

			# prone to error if incomplete rule
			# remember to check first longest rules
			if node.children:
				break

		if not node.children:
			node = None

		return node, result_index
