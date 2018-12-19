#!/usr/bin/python3
import ply.lex as lex
import sys

keywords = {

	'open' : 'OPEN',#

	'double' : 'DOUBLE',
	'float' : 'FLOAT',

	'bool' : 'BOOL',
	'int' : 'INT',
	'long' : 'LONG',
	'char' : 'CHAR',
	'string' : 'STRING',

	'let' : 'LET',
	'in' : 'IN',

	'else' : 'ELSE',
	'if' : 'IF',
	'then' : 'THEN',

	'TRUE' : 'TRUE',
	'FALSE' : 'FALSE',

	'begin' : 'BEGIN',
	'end' : 'END',

	'for' : 'FOR',
	'while' : 'WHILE',
	'do' : 'DO',
	'done' : 'DONE',
	'downto' : 'DOWNTO',
	'upto' : 'UPTO',

	'mod' : 'MOD',
	'and' : 'AND',
	'or' : 'OR',

	'print_int' : 'PRINT_INT',
	'print_str' : 'PRINT_STR',
	'return' : 'RETURN'
}


tokens = [
	'IDENTIFIER', 'NUM', 'CHAR_LITERAL', 'STRING_LITERAL',

	'MEMBERACCESS', 'PLUSPLUS', 'MINUSMINUS', 'ARROW',
	'NOT', 'LNOT',
	'MULT', 'DIVIDE',
	'PLUS', 'MINUS',
	'LT', 'GT', 'LTEQ', 'GTEQ',
	'EQ', 'NE',
	 'AND', 'OR',
	'EQUALS', 'ASSIGN',

	'LPAREN', 'RPAREN', 'ENDCOLON', 'ENDFUNCTION',
	'NEWLINE', 'COMMENT', 'PREPROCESSOR'

] + list(keywords.values())

t_ignore = ' \t\x0c'

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


t_MEMBERACCESS		= r'\.'

t_PLUSPLUS			= r'\+\+'
t_MINUSMINUS		= r'--'

t_ASSIGN			= r'<-'
t_NOT 				= r'~'
t_LNOT				= r'!'

t_MULT				= r'\*'
t_DIVIDE 			= r'/'
t_PLUS  			= r'\+'
t_MINUS 			= r'-'

t_LT				= r'<'
t_GT				= r'>'
t_LTEQ 				= r'<='
t_GTEQ 				= r'>='
t_EQ   				= r'=='
t_NE   				= r'!='

t_EQUALS     		= r'='

t_LPAREN           = r'\('
t_RPAREN           = r'\)'

t_ENDCOLON 		   = r';'
t_ENDFUNCTION		   = r';;'


def t_IDENTIFIER(t):
	r'[a-zA-Z_@][a-zA-Z_0-9]*'
	t.type = keywords.get(t.value,'IDENTIFIER')    #  Check for keywords words
	return t

t_NUM = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

t_CHAR_LITERAL = r'(L)?\'([^\\\n]|(\\.))*?\''

def t_COMMENT(t):
	r' /\*(.|\n)*?\*/'
	t.lineno += t.value.count('\n')

def t_PREPROCESSOR(t):
	r'\#(.)*?\n'
	t.lineno += 1


def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


#  Building the lexer
lexer = lex.lex()
