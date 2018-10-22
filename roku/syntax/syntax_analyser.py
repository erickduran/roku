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
		
	def start_analysis(self):
		result = self.check(':s', 0)
		print('result: ' + str(result))
		print('expected: ' + str(self.__length))

	def load_rules(self, path):
		file = open(path, 'r')
		self.__rules = json.load(file)
		
	def check(self, rule, i):
		if not rule.startswith(':'):
			if isinstance(self.__tuples[i], tuple):
				if self.__tuples[i][0] == rule:
					return i + 1
			else:
				if self.__tuples[i] == rule:
					return i + 1

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
			message = 'syntax error'
			raise SyntaxError(message)

		return result_index