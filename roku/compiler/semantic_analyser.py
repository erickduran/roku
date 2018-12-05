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
					rule = self.__rules['rules'][core]['options'][parent.rule]

					identifier_type = self.check_type(parent.children[0])
					value_type = self.check_type(parent.children[2])

					identifier = parent.children[0].core[2]
					identifier_raw_type = self.__identifier_table[identifier]
					
					parent.type = identifier_raw_type
					if value_type in self.__rules['compatibilities'][identifier_raw_type]:
						parent.type = identifier_raw_type
					else:
						raise TypeError(f'\'{identifier_raw_type}\' not compatible with \'{value_type}\' on line {parent.children[0].core[0][1]}.')
						
				if len(rule) > 1:
					# print('here')
					self.check_children(parent)
				else:
					parent.type = self.check_type(parent.children[rule[0]])
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

