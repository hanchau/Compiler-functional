#!/usr/bin/python3
from copy import deepcopy


class scope:
	def __init__(self):
		self.curr_table = table(None)
		# global temp_count
		# global label_count
		global base_table
		base_table = self.curr_table
		self.label_count = 0
		self.temp_count = 0

	def maketemp(self, temp_type, table):
		success = False
		while not success:
			name = "t"+str(self.temp_count)
			self.temp_count += 1
			success = table.insert_temp(temp_type, name)
		return name


	# Labels
	def newlabel(self):
		label = "L"+str(self.label_count)
		self.label_count += 1
		return label

	def begin_scope(self):
		new_table = table(self.curr_table)
		self.curr_table.children.append(new_table)
		self.curr_table = new_table
		return self.curr_table

	def end_scope(self):
		self.curr_table = self.curr_table.parent

	def insert_variable(self, var_type, identifier):
		self.curr_table.insert_variable(var_type, identifier)

	def insert_temp(self, var_type, identifier):
		self.curr_table.insert_temp(var_type, identifier)

	def lookup(self, identifier, table):
		if table != None:
			v = table.lookup_in_this(identifier)
			if v == None:
				return self.lookup(identifier, table.parent)
			return v
		else:
			return None


	def insert_function(self, method_name, return_type, param_types, param_num):
		self.curr_table.insert_function(method_name, return_type, param_types, param_num)

	def lookup_in_this(self, identifier):
		self.curr_table.lookup_in_this(identifier)

	def print_symbol_table(self, t):
		t.print_symbol_table()
		for c in t.children:
			self.print_symbol_table(c)
