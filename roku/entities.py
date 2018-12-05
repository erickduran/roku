class Node:
	def __init__(self, core):
		self.core = core
		self.type = None
		self.rule = None
		self.children = []

		# file = open('resources/semantic_rules.json', 'r')
		# self.__rules = json.load(file)



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

	# def type(self):
	# 	if self.type is not None:
	# 		return self.type
	# 	else:
	# 		if not self.children:
	# 			self.type = self.__rules['rules'][self.core[2]]
	# 			return self.type