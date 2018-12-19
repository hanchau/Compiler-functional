#!/usr/bin/python

import ply.lex as lex
from sys import argv
import os

token_count = {}

class MyLexer(object):

	keywords = ('open', 'include',   									#Modular
		'read_int', 'read_line',										#Input
		'print_string', 'print_int','print_float','print_char',			#Output
		'int', 'char', 'float', 'bool',									#Variable types
		'true', 'false',												#Bool
		'begin', 'end',													#Block
		'if', 'then', 'else',											#Conditional
		'while', 'for', 'to', 'downto', 'do', 'done',					#Loop Structures
		'let', 'in', 													#Let binding
		'ref',															#Pointer
		'mod'
		
	)

	tokens = [
		    

		'IDENT',
		'NUM',
		'CHAR_LITERAL',
		'STRING_LITERAL',

		'OR', 'AND',
		'NEQ', 'GTEQ', 'LTEQ',
		
		'ASSIGN',

		'LARR', 'RARR',
	
		'ENDCOLON',
		'PLUSPLUS', 'MINUSMINUS', 'EXPONENT',



	] + [k.upper() for k in keywords]
 
	literals = '()+-*/=?:,.^|&~!=[]{};<>@%'
	
	
	
	for token in tokens:
		token_count[str(token)] = [0,[]]
		
	for token in literals:
		token_count[str(token)] = [0,[]]


	def t_IDENT(self,t):
		'[A-Za-z_$][A-Za-z0-9_$]*'
		if t.value in MyLexer.keywords:
			t.type = t.value.upper()

		return t



	t_NUM = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
	t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
	t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

	t_OR = r'\|\|'
	t_AND = '&&'


	t_NEQ = '<>'
	t_GTEQ = '>='
	t_LTEQ = '<='

	t_ASSIGN = '<-'

	t_LARR = '\[\|'
	t_RARR = '\|\]'
	
	t_ENDCOLON = ';;'

	t_PLUSPLUS = r'\+\+'
	t_MINUSMINUS = r'\-\-'
	
	t_EXPONENT = '\*\*'

	t_ignore = ' \t\f'

	t_ignore_LINE_COMMENT = '///.*'

	#(*...*)in OCaml
	def t_BLOCK_COMMENT(self,t):
		r'\(\*(.|\n)*?\*\)'
		t.lexer.lineno += t.value.count('\n')


	def t_newline(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)


	def t_error(self,t):
		print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
		t.lexer.skip(1)

			 
class Lexer(object):

	def __init__(self):
		self.lexer = lex.lex(module=MyLexer(), optimize=1)


	def read_file(self,str_file):
		if type(str_file) == str:
			str_file = open(str_file)
		content = str_file.read()
		str_file.close()

		return content

	def tokenize_file(self,file_):
		content = self.read_file(file_)

		return self.print_token(content)

	def print_token(self,content):
		self.lexer.input(content)
		for token in self.lexer:
			token_count[str(token.type)][0] += 1
			token_count[str(token.type)][1].append(token.value)
		for key,value in token_count.items():
			if(value[0] != 0):
				print(str(key) + "\t\tCount:\t" + str(value[0]) + "\t\tLexemes:" + str(value[1]))




if __name__=="__main__":

	# Testing
	lexer = Lexer()

	lexer.tokenize_file(argv[1])
