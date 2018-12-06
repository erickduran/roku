# entities.py
"""This is a class where general entity classes will be declared.

The main objective of this class is to provide a place where simple
entities can be declared and referenced from.

"""
class Node:
	def __init__(self, core):
		self.core = core
		self.type = None
		self.rule = None
		self.children = []

	def append(self, node):
		self.children.append(node)

	def remove_children(self):
		self.children = []

	def length(self):
		total = 0
		if not self.children:
			total = 1
		else:
			for child in self.children:
				total += child.length()
		return total

	def copy(self):
		node = Node(self.core)
		node.children = self.children
		node.rule = self.rule
		return node
