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

class SyntaxAnalyser:
	def __init__(self, tuples):
		self.__tuples = tuples
		self.__length = len(tuples)
		self.__rules = []
		self.__last_correct_tuple = None
		
	def start_analysis(self):
		result = self.check(':s', 0)
		print('result: ' + str(result))
		print('expected: ' + str(self.__length))

	def load_rules(self, path):
		file = open(path, 'r')
		self.__rules = json.load(file)
		
	def check(self, rule, i):
		if not rule.startswith(':'):
			if self.__tuples[i][1] == rule:
				return i + 1
			else:
				self.__last_correct_tuple = self.__tuples[i]
				return None

		rule = self.__rules[rule]
		result_index = None
		for option in rule['rule_options']:
			result_index = i
			for rule in option:
				result_index = self.check(rule, result_index)

				if result_index is None:
					break

		if result_index is None:
			message = f'syntax error on line {self.__last_correct_tuple[0][1]}:{self.__last_correct_tuple[0][0]}'
			raise SyntaxError(message)

		return result_index