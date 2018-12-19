#!/usr/bin/python3
from copy import deepcopy


base_table = None

# Types
class type:
	def __init__(self, name, isbasic, isarray, ispointer, width, elem_type, length):
		self.name = name
		self.isbasic = isbasic
		self.isarray = isarray
		self.ispointer = ispointer
		self.width = width
		self.elem_type = elem_type
		self.length = length

	def type_name(self):
		if self.isbasic:
			return self.name
		elif self.isarray:
			return "array of " + self.elem_type.type_name() + ", length " + str(self.length)
