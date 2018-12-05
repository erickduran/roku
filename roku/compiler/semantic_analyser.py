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
						raise SemanticError(f'Variable \'{identifier}\' already declared.')

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
						rule = rule[:-1]

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
						if initial_type != 'INT' or initial_type != 'FLOAT':
							raise TypeError(f'\'{initial_type}\' not compatible with \'{operator}\' operator.')
					
					if parent.rule == 0:
						other_operation = parent.children[3]
						other_operator = other_operation.children[0].core[2]
						other_operating_type = self.check_type(other_operation.children[1])

						if other_operating_type != 'FLOAT' and other_operating_type != 'STRING' and other_operating_type != 'CHAR' and other_operating_type != 'INT':
							raise TypeError(f'Type \'{other_operating_type}\' not compatible with operation.')

						types = [initial_type, other_operating_type]
						second_type = None

						if 'FLOAT' in types:
							if 'CHAR' not in types and 'STRING' not in types:
								second_type = 'FLOAT'
							else:
								raise TypeError(f'\'CHAR|STRING\' not compatible with \'FLOAT\'.')
						elif 'STRING' in types:
							for element in types:
								if element != 'STRING':
									raise TypeError(f'\'{element}\' not compatible with \'STRING\'.')
							second_type = 'STRING'
						elif 'CHAR' in types:
							for element in types:
								if element != 'CHAR':
									raise TypeError(f'\'{element}\' not compatible with \'CHAR\'.')
							second_type = 'CHAR'
						elif 'INT' in types:
							for element in types:
								if element != 'INT':
									raise TypeError(f'\'{element}\' not compatible with \'INT\'.')
							second_type = 'INT'
						else:
							raise TypeError(f'Type not compatible with operation.')
						
						if operator != '+':
							if operator == '%' and second_type != 'INT':
								raise TypeError(f'\'{second_type}\' not compatible with \'{operator}\' operator.')
							if second_type != 'INT' or second_type != 'FLOAT':
								raise TypeError(f'\'{second_type}\' not compatible with \'{operator}\' operator.')

						parent.type = second_type

					else:
						parent.type = initial_type
				elif core == ':logical_operation':
					parent.type = 'BOOLEAN'
				elif core == ':logical_value':
					value_type = self.check_type(parent.children[rule[0]])
					if value_type != 'BOOLEAN':
						raise TypeError(f'\'{value_type}\' not compatible with \'{operator}\' operator.')
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

				if len(rule) == 1:
					if not parent.type:
						parent.type = self.check_type(parent.children[rule[0]])
				
				if len(parent.children) > 1:
					self.check_children(parent)
				return parent.type
		elif core == 'identifier':
			identifier = parent.core[2]
			if identifier in self.__identifier_table.keys():
				parent.type = self.__rules['rules'][self.__identifier_table[identifier]]['type']
				return parent.type
			else:
				raise SemanticError(f'Variable \'{identifier}\' referenced before assignment.')
		elif core == 'type':
			parent.type = self.__rules['rules'][parent.core[2]]['type']
			return parent.type
		else: 
			self.check_children(parent)
	
	def check_children(self, parent):
		for child in parent.children:
			if not child.type:
				self.check_type(child)

