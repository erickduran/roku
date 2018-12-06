# tuple_generator.py

from entities import Node

class TupleGenerator:
	
	def __init__(self):
		self.temp_count = 0
		self.label_count = 0
		self.tuples = [[]]

	def create_function_tuples(self, parent):
		context = [parent.children[1].core[2]]
		if parent.rule == 0:
			self.program_tuples(parent.children[8], context)
		if parent.rule == 1:
			self.program_tuples(parent.children[6], context)
		if parent.rule == 2:
			self.program_tuples(parent.children[7], context)
		if parent.rule == 3:
			self.program_tuples(parent.children[5], context)
		
		return context

	def create_tuples(self, parent):
		tuples = [[]]
		if (parent.core == ":s"):
			if (parent.rule == 0):
				context = ['energy']
				(self.program_tuples(parent.children[8], context))
				tuples[0] = context

				child = parent.children[0]
				tuples.append(self.create_function_tuples(child.children[0]))
				while child.rule == 0:
					child = child.children[1]
					tuples.append(self.create_function_tuples(child.children[0]))

			else:
				context = ['energy']
				self.program_tuples(parent.children[7], context)
				tuples[0] = context

		return tuples

	def create_instruction_tuples(self, parent, context):
		if parent.rule == 0:
			return self.assignment_tuple(self.get_value(parent.children[1], context), context[0] + '.result')
		if parent.rule == 4:
			return ('cabbage', None, None, None)

		else:
			return self.get_instruction_tuples(parent.children[0], context)

	def get_instruction_tuples(self, parent, context):
		if parent.core == ':declaration':
			return self.declare(parent, context)
		if parent.core == ':call':
			return self.create_function_call_tuples(parent, context)
		if parent.core == ':assignment':
			return self.assignment_tuple(self.get_value(parent.children[2], context), parent.children[0].core[2])
		if parent.core == ':flow':
			return self.if_block(parent, context)
		if parent.core == ':loop':
			if parent.rule == 0:
				return self.for_block(parent.children[0], context)
			if parent.rule == 1:
				return self.while_block(parent.children[0], context)

	def program_tuples(self, parent, context):
		context.append(self.create_instruction_tuples(parent.children[0], context))
		
		child = parent
		while child.rule == 0:
			child = child.children[1]
			context.append(self.create_instruction_tuples(child.children[0], context))

	def assignment_tuple(self, value, name):
		return ('assign', value, '-', name)
	
	def declare(self, node, context):
		if node.rule == 0:
			return self.assignment_tuple(self.get_value(node.children[1].children[2], context), node.children[1].children[0].core[2])
		if node.rule == 1:
			return self.assignment_tuple(0 if node.type == 'INT' else "" , node.children[1].core[2])

	def create_function_call_tuples(self, node, context):
		if node.rule == 0: # With args
			arg_count = 1
			args_node = node.children[2]
			context.append(self.assignment_tuple(self.get_value(args_node.children[0], context), 
												 node.children[0].core[2] + '.arg' + str(arg_count)))
			arg_count += 1
			if args_node.rule == 0:
				args_node = args_node.children[1]
				context.append(self.assignment_tuple(self.get_value(args_node.children[1], context), 
													node.children[0].core[2] + '.arg' + str(arg_count)))
				arg_count += 1

				while args_node.rule == 0:
					args_node = args_node.children[2]
					context.append(self.assignment_tuple(self.get_value(args_node.children[1], context), 
														node.children[0].core[2] + '.arg' + str(arg_count)))
					arg_count += 1

		# Make call
		return self.run_tuple(node.children[0].core[2])

	def get_value(self, node, context):
		if node.rule == 0: # Number
			return node.children[0].children[0].core[2]

		elif node.rule == 1: # Operation
			operation = node.children[0]
			if operation.rule == 1:
				return self.operation(operation, context)

		elif node.rule == 3: # call
			func_call = node.children[0]
			self.create_function_call_tuples(func_call, context)
			return func_call.children[0].core[2] + '.result'

		elif node.rule == 4: #logical
			return self.create_logical_tuples(node.children[0], context)

		elif node.rule == 5:
			return node.children[0].core[1]

		else: # Any other constant or identifier
			return node.children[0].core[2]

	def create_logical_tuples(self, node, context): 
		if node.rule == 0: #log operation 
			logical_op = node.children[0]
			return self.create_logical_operation(logical_op, context)
			
		if node.rule == 1: #logical value
			return self.get_logical_value(node.children[0], context)

	def create_logical_operation(self, node, context):
		if node.rule == 0: #one element
			element_1 = self.get_logical_value(node.children[0], context)
			element_2 = self.get_logical_value(node.children[2], context)
			result = self.next_temp()
			context.append((node.children[1].core[2], element_1, element_2, result))
			return result 
		else: #more elements
			element_1 = self.get_logical_value(node.children[0], context)
			element_2 = self.create_logical_operation(node.children[2], context)
			result = self.next_temp()
			context.append((node.children[1].core[2], element_1, element_2, result))
			return result

	def get_logical_value(self, node, context):
		if node.rule == 0: #comparison
			element_1 = self.get_comparing(node.children[0].children[0], context)
			element_2 = self.get_comparing(node.children[0].children[2], context)
			result = self.next_temp()
			context.append((node.children[0].children[1].core[2], element_1, element_2, result))
			return result
		if node.rule == 1: # negation 
			original_result = self.create_logical_tuples(node.children[0].children[1], context)
			negated_result = self.next_temp()
			context.append(('not', original_result, None, negated_result))
			return negated_result
		if node.rule == 2: # koi
			return node.children[0].core[2]
		if node.rule == 3: # identifier
			return node.children[0].core[2]
		if node.rule == 4: # call
			func_call = node.children[0]
			self.create_function_call_tuples(func_call, context)
			return func_call.children[0].core[2] + '.result'
	
	def get_comparing(self, node, context):
		if node.rule == 0: # Number
			return node.children[0].children[0].core[2]
		if node.rule == 2: # Call
			func_call = node.children[0]
			self.create_function_call_tuples(func_call, context)
			return func_call.children[0].core[2] + '.result'
		elif node.rule == 5: # operation
			return self.operation(node.children[0], context)
		elif node.rule == 6: # sokka
			return node.children[0].core[1]
		else: #anything else
			return node.children[0].core[2]

	def operation(self, operation, context):
		element_1 = self.get_operating(operation.children[0], context)
		element_2 = self.get_operating(operation.children[2], context)
		temp = self.next_temp()
		context.append((operation.children[1].core[2], element_1, element_2, temp))
		return temp

	def get_operating(self, node, context):
		if node.rule == 0: # Number
			return node.children[0].children[0].core[2]
		elif node.rule == 2: # Call
			func_call = node.children[0]
			self.create_function_call_tuples(func_call, context)
			return func_call.children[0].core[2] + '.result'
		else: # Anything else
			return node.children[0].core[2]

	def while_block(self, node, context):
		start_label = self.next_label()
		end_label = self.next_label()
		
		condition = self.create_logical_tuples(node.children[2], context)
		context.append(('iftrue', condition, None, start_label))
		context.append(('iffalse', condition, None, end_label))

		context.append(start_label)
		self.program_tuples(node.children[5], context)
		condition = self.create_logical_tuples(node.children[2], context)
		context.append(('iftrue', condition, None, start_label))
		return end_label

	def for_block(self, node, context):
		start_label = self.next_label()
		end_label = self.next_label()

		context.append(self.get_instruction_tuples(node.children[2], context))

		condition = self.create_logical_tuples(node.children[4], context)

		context.append(('iftrue', condition, None, start_label))
		context.append(('iffalse', condition, None, end_label))

		context.append(start_label)
		self.program_tuples(node.children[9], context)
		context.append(self.get_instruction_tuples(node.children[6], context))

		condition = self.create_logical_tuples(node.children[4], context)
		context.append(('iftrue', condition, None, start_label))

		return end_label
		

	def if_block(self, node, context):
		self.create_agni_tuples(node.children[0], context)
		agni_end_label = self.current_label()
		block_end_label = self.next_label()
		context.append(('goto', None, None, block_end_label))
		context.append(agni_end_label)

		if node.rule == 0:
			self.create_agnikai_tuples(node.children[1], context, block_end_label)
			self.create_kai_tuples(node.children[2], context)
		if node.rule == 1:
			self.create_agnikai_tuples(node.children[1], context, block_end_label)
		if node.rule == 2:
			self.create_kai_tuples(node.children[1])

		return block_end_label

	def create_agnikai_tuples(self, node, context, block_end):
		agnikai = node.children[0]
		start_label = self.next_label()
		end_label = self.next_label()
		condition = self.create_logical_tuples(agnikai.children[2], context)
		context.append(('iftrue', condition, None, start_label))
		context.append(('iffalse', condition, None, end_label))

		context.append(start_label)
		if agnikai.rule == 0:
			self.program_tuples(agnikai.children[5], context)
		context.append(('goto', None, None, block_end))
		context.append(end_label)

		
		if node.rule == 1:
			self.create_agnikai_tuples(node.children[1], context, block_end)

	def create_kai_tuples(self, node, context):
		if node.rule == 0:
			self.program_tuples(node.children[2], context)

	def create_agni_tuples(self, node, context):
		start_label = self.next_label()
		end_label = self.next_label()
		condition = self.create_logical_tuples(node.children[2], context)
		context.append(('iftrue', condition, None, start_label))
		context.append(('iffalse', condition, None, end_label))

		context.append(start_label)
		if node.rule == 0:
			self.program_tuples(node.children[5], context)


	def next_temp(self):
		self.temp_count += 1
		temp = 'T' + str(self.temp_count)
		return temp

	def next_label(self):
		self.label_count += 1
		label = 'L' + str(self.label_count)
		return label
	
	def current_label(self):
		return 'L' + str(self.label_count)

	def run_tuple(self, label):
		return ('run', None, None, label)