class Node:
	def __init__(self, core):
		self.core = core
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
		return node