# syntax_analyser.py
import json

from entities import Node
from errors import TypeError, SemanticError

class SemanticAnalyser:

	def __init__(self):
		self.__identifier_table = dict()
		self.__rules = []

	def load_rules(self, path):
		file = open(path, 'r')
		self.__rules = json.load(file)

	def check_type(self, parent):
		if parent.type:
			return parent.type
		core = None
		if isinstance(parent.core, tuple):
			core = parent.core[1]
		else:
			core = parent.core
		if core in self.__rules['rules']:
			if self.__rules['rules'][core]['final']:
				parent.type = self.__rules['rules'][core]['type']
				return parent.type
			else:
				rule = self.__rules['rules'][core]['options'][parent.rule]

				if core == ':declaration':
					identifier = None
					type_check = self.check_type(parent.children[rule[0]])
					if parent.rule == 0:
						assignment = parent.children[1]
						identifier = assignment.children[0].core[2]

					else:
						identifier = parent.children[1].core[2]

					if identifier in self.__identifier_table.keys():
						if not isinstance(self.__identifier_table[identifier], dict):
							raise SemanticError(f'Variable \'{identifier}\' already declared.')
						raise SemanticError(f'Identifier \'{identifier}\' already used in function.')

					self.__identifier_table[identifier] = parent.children[rule[0]].core[2]
					if parent.rule == 0:
						self.check_type(parent.children[rule[1]])

					parent.type = type_check
					if parent.rule == 0:
						parent.children[1].children[0].type = self.check_type(parent.children[1].children[0])
					else:
						parent.children[1].type = self.check_type(parent.children[1])
				elif core == ':assignment':
					identifier_raw_type = self.check_type(parent.children[0])
					value_type = self.check_type(parent.children[2])

					identifier = parent.children[0].core[2]
					identifier_type = self.__identifier_table[identifier]
					
					parent.type = identifier_type
					if value_type in self.__rules['compatibilities'][identifier_type]:
						parent.type = value_type
					else:
						raise TypeError(f'\'{identifier_type}\' not compatible with \'{value_type}\' on line {parent.children[0].core[0][1]}.')
				elif core == ':operation':
					types = []
					operator = parent.children[1].core[2]

					if parent.rule == 0:
						raise SemanticError('Operations with more than 2 elements are currently not supported.')

					for element in rule:
						node = parent.children[element]
						types.append(self.check_type(node))

					initial_type = None
					
					if 'FLOAT' in types:
						if 'CHAR' not in types and 'STRING' not in types:
							initial_type = 'FLOAT'
						else:
							raise TypeError(f'\'CHAR|STRING\' not compatible with \'FLOAT\'.')
					elif 'STRING' in types:
						for element in types:
							if element != 'STRING':
								raise TypeError(f'\'{element}\' not compatible with \'STRING\'.')
						initial_type = 'STRING'
					elif 'CHAR' in types:
						for element in types:
							if element != 'CHAR':
								raise TypeError(f'\'{element}\' not compatible with \'CHAR\'.')
						initial_type = 'CHAR'
					elif 'INT' in types:
						for element in types:
							if element != 'INT':
								raise TypeError(f'\'{element}\' not compatible with \'INT\'.')
						initial_type = 'INT'
					else:
						raise TypeError(f'Type not compatible with operation.')
					
					if operator != '+':
						if operator == '%' and initial_type != 'INT':
							raise TypeError(f'\'{initial_type}\' not compatible with \'{operator}\' operator.')
						if initial_type != 'INT' and initial_type != 'FLOAT':
							raise TypeError(f'\'{initial_type}\' not compatible with \'{operator}\' operator.')
					parent.type = initial_type
				elif core == ':logical_value':
					# print(parent.children[rule[0]].core)
					value_type = self.check_type(parent.children[rule[0]])
					if value_type != 'BOOLEAN':
						raise TypeError(f'\'{value_type}\' not compatible with \'BOOLEAN\'.')
					parent.type = value_type		
				elif core == ':comparison':
					types = []
					operator = parent.children[1].core[2]

					for element in rule:
						node = parent.children[element]
						types.append(self.check_type(node))

					numeric_operators = ['<=', '>=', '>', '<']
					if operator in numeric_operators:
						for element in types:
							if element not in ['INT', 'FLOAT']:
								raise TypeError(f'\'{element}\' not compatible with \'{operator}\' operator.')
								
					parent.type = 'BOOLEAN'
				elif core == ':function':
					type_node = None
					identifier_type = 'sokka'
					type_check = None

					if rule:
						type_node = parent.children[rule[0]]

					if type_node:
						identifier_type = type_node.core[2]
						type_check = self.check_type(type_node)

					identifier = parent.children[1].core[2]

					if identifier in self.__identifier_table.keys():
						if isinstance(self.__identifier_table[identifier], dict):
							raise SemanticError(f'Function \'{identifier}\' already declared.')
						raise SemanticError(f'Identifier \'{identifier}\' already used in variable.')
						
					self.__identifier_table[identifier] = dict()
					self.__identifier_table[identifier]['type'] = identifier_type

					if parent.rule == 0 or parent.rule == 1:
						args_node = parent.children[3]
						args_types = self.check_type(args_node)
						self.__identifier_table[identifier]['args_types'] = args_types

					parent.type = type_check
				elif core == ':logical_operation':
					parent.type = 'BOOLEAN'
				if rule:
					if len(rule) == 1:
						if not parent.type:
							parent.type = self.check_type(parent.children[rule[0]])
				
				if len(parent.children) > 1:
					self.check_children(parent)

				return parent.type
		elif core == 'identifier':
			identifier = parent.core[2]
			if identifier in self.__identifier_table.keys():
				if not isinstance(self.__identifier_table[identifier], dict):
					parent.type = self.__rules['rules'][self.__identifier_table[identifier]]['type']
					return parent.type
			else:
				raise SemanticError(f'Variable \'{identifier}\' referenced before assignment.')
		elif core == 'type':
			parent.type = self.__rules['rules'][parent.core[2]]['type']
			return parent.type
		elif core == ':args':
			nodes = []
			nodes.append(parent.children[0].children[0].core[2])
			if parent.rule == 0:
				nodes.extend(self.check_type(parent.children[1]))
			return nodes
		elif core == ':argses':
			nodes = []
			nodes.append(parent.children[1].children[0].core[2])
			if parent.rule == 0:
				nodes.extend(self.check_type(parent.children[2]))
			return nodes
		elif core == ':call':
			identifier = parent.children[0].core[2]
			if identifier in self.__identifier_table.keys():
				if isinstance(self.__identifier_table[identifier], dict):
					if 'args_types' in self.__identifier_table[identifier].keys():
						expected_args = self.__identifier_table[identifier]['args_types']
						if parent.rule == 0:
							args_raw_types = self.check_type(parent.children[2])
							if len(args_raw_types) != len(expected_args):
								raise SemanticError(f'Missing arguments for functions, expected: {str(expected_args)}.')
							for i, arg_type in enumerate(args_raw_types):
								if arg_type not in self.__rules['compatibilities'][expected_args[i]]:
									raise TypeError(f'Incompatible arguments in call, expected: {str(expected_args)}.')
						else:
							raise SemanticError(f'Missing arguments for functions, expected: {str(expected_args)}.')
					function_type = self.__identifier_table[identifier]['type']
					parent.type = self.__rules['rules'][function_type]['type']
					return parent.type
			raise SemanticError(f'Function \'{identifier}\' not declared.')
		elif core == ':args_call':
			nodes = []
			nodes.append(self.check_type(parent.children[0]))
			if parent.rule == 0:
				nodes.extend(self.check_type(parent.children[1]))
			return nodes
		elif core == ':args_calls':
			nodes = []
			nodes.append(self.check_type(parent.children[1]))
			if parent.rule == 0:
				nodes.extend(self.check_type(parent.children[2]))
			return nodes
		else: 
			self.check_children(parent)
		

	def check_children(self, parent):
		for child in parent.children:
			if not child.type:
				self.check_type(child)

