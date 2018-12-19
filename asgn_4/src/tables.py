#!/usr/bin/python3
from copy import deepcopy
from types import *
class table:
	def __init__(self, prev = None):
		self.hash = {}
		self.width = 0
		self.parent = prev
		self.children = []

	def insert_variable(self, var_type, identifier):
		self.hash[identifier] = {}
		self.hash[identifier]['type'] = var_type
		self.hash[identifier]['category'] = 'variable'

	def insert_temp(self, var_type, identifier):
		if identifier not in self.hash:
			self.hash[identifier] = {}
			self.hash[identifier]['type'] = var_type
			self.hash[identifier]['category'] = 'temporary'
			return True
		else:
			return False

	def insert_function(self, method_name, return_type, param_types, param_num):
		if method_name not in self.hash:
			self.hash[method_name] = {}
			self.hash[method_name]['type'] = return_type
			self.hash[method_name]['category'] = 'function'
			self.hash[method_name]['arg_num'] = param_num
			self.hash[method_name]['arg_types'] = param_types


	def lookup_in_this(self, identifier):
		if identifier in self.hash:
			return self.hash[identifier]
		else:
			return None

	def print_symbol_table(self):
		print("")
		for key in self.hash:
			print("NAME: ", key)
			for k in self.hash[key]:
				if k == 'type' and not isinstance(self.hash[key][k], str):
					print(k, ': ', self.hash[key][k].type_name())
				elif k == 'arg_types':
					types = []
					for t in self.hash[key][k]:
						if not isinstance(t, str):
							types.append(t.type_name())
						else:
							types.append(t)
					print(k, ': ', types)
				else:
					print(k, ': ', self.hash[key][k])
			print("")
