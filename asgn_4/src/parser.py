#!/usr/bin/python3
import sys
import ply.yacc as yacc
from lexer import *
from copy import deepcopy
import symtab
import tac

symbol_table = symtab.scope()

if len(sys.argv) == 2:
	filename = sys.argv[1]
else:
	print("Usage: ./parser file.cs")
	exit(0)



# OC.1  Precedence and associativity of operators
precedence = (
	('left', 'EQUALS'),
	('left', 'OR'),
	('left', 'AND'),
	('left', 'EQ', 'NE'),
	('left', 'GT', 'GTEQ', 'LT', 'LTEQ'),
	('left', 'PLUS', 'MINUS'),
	('left', 'MULT', 'DIVIDE', 'MOD'),
	('right', 'NOT', 'LNOT'),
	('left', 'MEMBERACCESS')
)

# OC.2 Syntactic grammar


# OC.2.1 Basic concepts
def p_module_name(p):
	"""module_name : IDENTIFIER
	"""

# OC.2.2 Types
def p_type(p):
	"""type : non_array_type
	"""
	p[0] = deepcopy(p[1])

def p_non_array_type(p):
	"""non_array_type : numeric_type
	"""
	p[0] = deepcopy(p[1])

def p_numeric_type(p):
	"""numeric_type : integral_type
	"""
	p[0] = deepcopy(p[1])

def p_integral_type(p):
	"""integral_type : INT
					| CHAR
	"""
	if p[1] == 'int':
		p[0] = symtab.type('int', True, False, False, 4, None, None)
	elif p[1] == 'char':
		p[0] = symtab.type('char', True, False, False, 1, None, None)



# OC.2.3 Expressions
def p_function_call_paren_endcolon(p):
	"""function_call_paren_endcolon : function_call_paren ENDCOLON
	"""
	p[0] = deepcopy(p[1])
def p_function_call_paren(p):
	"""function_call_paren : function_call
	"""
	p[0] = deepcopy(p[1])

def p_function_call(p):
	"""function_call : IDENTIFIER LPAREN argument_list_or_empty RPAREN
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value'] = None
	no_of_args = 0
	name = symbol_table.lookup(p[1], symbol_table.curr_table)
	if name != None:
		if name['category'] == 'function':
			if p[3] != None:
				no_of_args = len(p[3])
			if name['arg_num'] != no_of_args:
				print("ERROR MESSAGE: Function '",p[1],"' has been defined over ", name['arg_num'], "parameters, Given arguments are '", len(p[3]),"'")
				print("COMPILATION HAS BEEN TERMINATED")
				exit()
			else:
				if no_of_args > 0:
					for arg in p[3]:
						p[0]['ir_code'] += ['param, ' + arg['value']]
				p[0]['ir_code'] += ['call, ' + p[1] + ', ' + str(no_of_args)]
		else:
			print("ERROR MESSAGE: Function '",p[1],"' has not been defined as category function, Line'", p.lineno(1),"'")
			print("COMPILATION HAS BEEN TERMINATED")
			exit()
	else:
		print("ERROR MESSAGE: Function '", p[1],"' has not been defined, Line '", p.lineno(1),"'")
		print("COMPILATION HAS BEEN TERMINATED")
		exit()


def p_argument_list_or_empty(p):
	"""argument_list_or_empty : argument_list
		| empty
	"""
	p[0] = deepcopy(p[1])
def p_argument_list(p):
	"""argument_list : argument
		| argument_list  argument
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1]) + [deepcopy(p[2])]
def p_argument(p):
	"""argument : IDENTIFIER
	"""
	var = symbol_table.lookup(p[1], symbol_table.curr_table)
	if var != None:
		p[0] = {}
		p[0]['ir_code'] = [""]
		p[0]['value'] = p[1]
	else:
		print("ERROR MESSAGE: symbol '",p[1],"' used without declaration")
		print("COMPILATION HAS BEEN TERMINATED")
		exit()


def p_primary_expression(p):
	"""primary_expression : parenthesized_expression
		| primary_expression_no_parenthesis
	"""
	p[0] = deepcopy(p[1])

def p_parenthesized_expression(p):
	"""parenthesized_expression : LPAREN expression RPAREN
	"""
	p[0] = deepcopy(p[2])

def p_primary_expression_no_parenthesis_a(p):
	"""primary_expression_no_parenthesis : literal
		| function_call_paren
	"""
	p[0] = deepcopy(p[1])

def p_primary_expression_no_parenthesis_b(p):
	"""primary_expression_no_parenthesis : IDENTIFIER
	"""
	var = symbol_table.lookup(p[1], symbol_table.curr_table)
	if var != None:
		p[0] = {}
		p[0]['ir_code'] = [""]
		p[0]['value'] = p[1]
	else:
		print("ERROR MESSAGE: symbol '",p[1],"' used without declaration")
		print("COMPILATION HAS BEEN TERMINATED")
		exit()



def p_literal(p):
	"""literal : NUM
				| CHAR_LITERAL
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value'] = p[1]

def p_postfix_expression(p):
	"""postfix_expression : primary_expression
	"""
	p[0] = deepcopy(p[1])

def p_pre_increment_expression(p):
	"""pre_increment_expression : PLUSPLUS postfix_expression
	"""
	t = symbol_table.maketemp('int', symbol_table.curr_table)
	p[0] = deepcopy(p[2])
	p[0]['ir_code'] += ["+, " + t + ", " + p[0]['value'] + ", 1 "]
	p[0]['ir_code'] += ["=, " + p[0]['value'] + ", " + t]

def p_pre_decrement_expression(p):
	"""pre_decrement_expression : MINUSMINUS postfix_expression
	"""
	t = symbol_table.maketemp('int', symbol_table.curr_table)
	p[0] = deepcopy(p[2])
	p[0]['ir_code'] += ["-, " + t + ", " + p[0]['value'] + ", 1 "]
	p[0]['ir_code'] += ["=, " + p[0]['value'] + ", " + t]
def p_unary_expression_not_plusminus(p):
	"""unary_expression_not_plusminus : postfix_expression
		| LNOT unary_expression
		| NOT unary_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = deepcopy(p[2])
		if p[1] == '!':
			p[0]['ir_code'] += ["!, " + p[0]['value']]
		elif p[1] == '~':
			p[0]['ir_code'] += ["~, " + p[0]['value']]

def p_unary_expression(p):
	"""unary_expression : unary_expression_not_plusminus
		| PLUS unary_expression
		| MINUS unary_expression
		| pre_increment_expression
		| pre_decrement_expression
	"""
	p[0] = {}
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		if p[1] == '+':
			p[0] = deepcopy(p[2])
		elif p[1] == '-':
			t = symbol_table.maketemp('int', symbol_table.curr_table)
			p[0]['value'] = t
			p[0]['ir_code'] = deepcopy(p[2]['ir_code'])
			p[0]['ir_code'] += ["-, " + p[0]['value'] + ", " + p[2]['value'] + ", 0"]

def p_multiplicative_expression(p):
	"""multiplicative_expression : unary_expression
		| multiplicative_expression MULT unary_expression
		| multiplicative_expression DIVIDE unary_expression
		| multiplicative_expression MOD unary_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		if p[2] == '*':
			p[0]['value'] = t
			p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
			p[0]['ir_code'] += ["*, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '/':
			p[0]['value'] = t
			p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
			p[0]['ir_code'] += ["/, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == 'mod':
			p[0]['value'] = t
			p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
			p[0]['ir_code'] += ["%, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]

def p_additive_expression(p):
	"""additive_expression : multiplicative_expression
		| additive_expression PLUS multiplicative_expression
		| additive_expression MINUS multiplicative_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
		if p[2] == '+':
			p[0]['ir_code'] += ["+, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '-':
			p[0]['ir_code'] += ["-, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]

def p_relational_expression(p):
	"""relational_expression : additive_expression
		| relational_expression LT additive_expression
		| relational_expression GT additive_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
		if p[2] == '<':
			p[0]['ir_code'] += ["<, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '>':
			p[0]['ir_code'] += [">, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]

def p_equality_expression(p):
	"""equality_expression : relational_expression
		| equality_expression EQ relational_expression
		| equality_expression NE relational_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
		if p[2] == '==':
			p[0]['ir_code'] += ["==, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '!=':
			p[0]['ir_code'] += ["!=, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]

def p_conditional_and_expression(p):
	"""conditional_and_expression : equality_expression
		| conditional_and_expression AND equality_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
		p[0]['ir_code'] += ["&&, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
def p_conditional_or_expression(p):
	"""conditional_or_expression : conditional_and_expression
		| conditional_or_expression OR conditional_and_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['ir_code'] = p[1]['ir_code'] + p[3]['ir_code']
		p[0]['ir_code'] += ["||, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
def p_assignment(p):
	"""assignment : unary_expression assignment_operator expression
	"""
	var = symbol_table.lookup(p[1]['value'], symbol_table.curr_table)
	if var != None:
		p[0] = {}
		p[0]['value'] = p[1]['value']
		p[0]['ir_code'] = p[3]['ir_code']
		p[0]['ir_code'] += p[1]['ir_code']
		p[0]['ir_code'] += ['=, ' + p[1]['value'] + ", " + p[3]['value']]
	else:
		print("ERROR MESSAGE: symbol '",p[1]['value'],"' used without declaration")
		print("COMPILATION HAS BEEN TERMINATED")
		exit()
def p_assignment_operator(p):
	"""assignment_operator : ASSIGN
							| EQUALS
	"""
	p[0] = deepcopy(p[1])
def p_expression(p):
	"""expression : conditional_or_expression
		| assignment
	"""
	p[0] = deepcopy(p[1])
def p_boolean_expression(p):
	"""boolean_expression : expression
		| TRUE
		| FALSE
	"""
	p[0] = deepcopy(p[1])


# OC.2.4 Statements
def p_statement(p):
	"""statement : declaration_statement
		| embedded_statement
		| print_statement
		| function_call_paren_endcolon
		| return_statement
	"""
	p[0] = deepcopy(p[1])

def p_print_statement(p):
	"""print_statement : print_int_statement
		| print_string_statement
	"""
	p[0] = deepcopy(p[1])
def p_print_int_statement(p):
	"""print_int_statement : PRINT_INT LPAREN expression RPAREN ENDCOLON
	"""
	p[0] = {}
	p[0]['value'] = p[3]['value']
	p[0]['ir_code'] = p[3]['ir_code']
	p[0]['ir_code'] += ['print, ' + p[3]['value'] ]
def p_print_string_statement(p):
	"""print_string_statement : PRINT_STR LPAREN STRING_LITERAL RPAREN ENDCOLON
	"""

def p_embedded_statement(p):
	"""embedded_statement : block
		| expression_statement
		| selection_statement
		| iteration_statement
	"""
	p[0] = deepcopy(p[1])

def p_block(p):
	"""block : BEGIN begin_scope statement_list_or_empty END
	"""
	p[0] = deepcopy(p[3])
	symbol_table.end_scope()

def p_statement_list_or_empty(p):
	"""statement_list_or_empty : empty
		| statement_list
	"""
	p[0] = deepcopy(p[1])

def p_statement_list(p):
	"""statement_list : statement
		| statement_list statement
	"""
	p[0] = deepcopy(p[1])
	if len(p) == 3:
		p[0]['ir_code'] += p[2]['ir_code']
		p[0]['value'] = None

def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration
	"""
	p[0] = deepcopy(p[1])

def p_global_variable_declaration(p):
	"""global_variable_declaration : LET variable_declarators IN
	"""
	p[0] = deepcopy(p[2])

def p_local_variable_declaration(p):
	"""local_variable_declaration : LET variable_declarators IN
	"""
	p[0] = deepcopy(p[2])


def p_variable_declarators(p):
	"""variable_declarators : type variable_declarator
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value'] = p[1]
	var_type = p[1]
	variable, value_init, line_no = p[2][0], p[2][1], p[2][2]
	if symbol_table.lookup_in_this(variable) != None:
		print("ERROR MESSAGE: This variable '",variable,"', has been declared before in this scope in line '",line_no,"' .")
		print("COMPILATION HAS BEEN TERMINATED")
		exit()
	else:
		if value_init != None:
			symbol_table.insert_variable(var_type, variable)
			p[0]['ir_code'] += value_init['ir_code']
			p[0]['ir_code'] += ["=, " + variable + ", " + value_init['value']]
		else:
			symbol_table.insert_variable(var_type, variable)
			p[0]['ir_code'] += [var_type.name + ", " + variable]

def p_variable_declarator(p):
	"""variable_declarator : IDENTIFIER
		| IDENTIFIER assignment_operator variable_initializer
	"""
	if len(p) == 2:
		p[0] = [p[1], None, p.lineno(1)]
	else:
		p[0] = [p[1], deepcopy(p[3]), p.lineno(1)]
def p_variable_initializer(p):
	"""variable_initializer :  expression
	"""
	p[0] = deepcopy(p[1])



def p_expression_statement(p):
	"""expression_statement : statement_expression ENDCOLON
	"""
	p[0] = deepcopy(p[1])

def p_statement_expression(p):
	"""statement_expression : empty
		| assignment
		| pre_increment_expression
		| pre_decrement_expression
		| function_call_paren
	"""
	p[0] = deepcopy(p[1])

def p_selection_statement(p):
	"""selection_statement : if_statement
	"""
	p[0] = deepcopy(p[1])

def p_if_statement(p):
	"""if_statement : IF boolean_expression THEN embedded_statement
		| IF boolean_expression THEN embedded_statement ELSE embedded_statement
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value'] = None
	if len(p) == 7:
		p[2]['if_true'] = symbol_table.newlabel()
		p[0]['next'] = symbol_table.newlabel()
		p[0]['ir_code'] += p[2]['ir_code']
		p[0]['ir_code'] += ['ifgoto, ==, ' + p[2]['value'] + ',1 ' + p[2]['if_true']]
		p[0]['ir_code'] += p[6]['ir_code']
		p[0]['ir_code'] += ['goto, ' + p[0]['next']]
		p[0]['ir_code'] += ['label, ' + p[2]['if_true']]
		p[0]['ir_code'] += p[4]['ir_code']
		p[0]['ir_code'] += ['label, ' + p[0]['next']]
	else:
		p[2]['False'] = symbol_table.newlabel()
		p[2]['if_true'] = symbol_table.newlabel()
		p[0]['ir_code'] += p[2]['ir_code']
		p[0]['ir_code'] += ['ifgoto, ==, ' + p[2]['value'] + '1, ' + p[2]['if_true']]
		p[0]['ir_code'] += ['goto, ' + p[2]['False']]
		p[0]['ir_code'] += ['label, ' + p[2]['if_true']]
		p[0]['ir_code'] += p[4]['ir_code']
		p[0]['ir_code'] += ['label, ' + p[2]['False']]

def p_iteration_statement(p):
	"""iteration_statement : while_statement
		| for_statement
	"""
	p[0] = deepcopy(p[1])

def p_while_statement(p):
	"""while_statement : WHILE  boolean_expression  DO embedded_statement DONE
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value'] = None
	p[0]['loop_start'] = symbol_table.newlabel()
	p[0]['loop_end'] = symbol_table.newlabel()
	p[2]['if_true'] = symbol_table.newlabel()
	p[0]['ir_code'] += ['label, ' + p[0]['loop_start']]
	p[0]['ir_code'] += p[2]['ir_code']
	p[0]['ir_code'] += ['ifgoto, ==, ' + p[2]['value'] + ", 1, " + p[2]['if_true']]
	p[0]['ir_code'] += ['goto, ' + p[0]['loop_end']]
	p[0]['ir_code'] += ['label, ' + p[2]['if_true']]
	p[0]['ir_code'] += p[4]['ir_code']
	p[0]['ir_code'] += ['goto, ' + p[0]['loop_start']]
	p[0]['ir_code'] += ['label, ' + p[0]['loop_end']]

def p_for_statement(p):
	"""for_statement : FOR IDENTIFIER EQUALS ident TO ident  DO embedded_statement DONE
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value'] = None
	p[0]['loop_start'] = symbol_table.newlabel()
	p[0]['ir_code'] += ['=, ' + p[2] +', '+ p[4]['value']]
	p[0]['ir_code'] += ['label, ' + p[0]['loop_start']]
	p[0]['ir_code'] += p[8]['ir_code']
	p[0]['ir_code'] += ['ifgoto, >, '+ p[2] +', '+ p[6]['value'] +', '+  p[0]['loop_start']]

def p_ident(p):
	"""ident : NUM
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value'] = p[1]

# OC.2.5 Compilation Unit
def p_compilation_unit(p):
	"""compilation_unit : module
	"""
	#print("PARSING started !!!")
	p[0] = p[1]
	#print("PARSING DONE !!!")

	#print("----------------------------------------------------------------------")
	#symbol_table.print_symbol_table(symtab.base_table)
	#print("")
	#print("----------------------------------------------------------------------")
	tac.print_tac(p[0])
	print("")

def p_module(p):
	"""module : open_directives_or_empty module_member_declarations
	"""
	p[0] = p[2]


def p_module_member_declarations(p):
	"""module_member_declarations : module_member_declaration
		| module_member_declarations module_member_declaration
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1]) + [deepcopy(p[2])]

def p_module_member_declaration(p):
	"""module_member_declaration : function_declaration
		| global_variable_declaration
	"""
	p[0] = deepcopy(p[1])

def p_open_directives_or_empty(p):
	"""open_directives_or_empty : empty
		| open_directives
	"""
def p_open_directives(p):
	"""open_directives : open_module
		| open_directives open_module
	"""
def p_open_module(p):
	"""open_module : OPEN module_names
	"""
def p_module_names(p):
	"""module_names : module_names module_name
		| module_name
	"""
# OC.2.6 functions


def p_function_declaration(p):
	"""function_declaration : function_header function_body
	"""
	return_type = 'int'
	function_name = p[1][1]
	function_params = p[1][2]
	function_body = p[2]
	p[0] = {'ir_code':[], 'value':None}
	p[0]['ir_code'] += ['function, ' + function_name]
	if function_params != None:
		for params in function_params:
			p[0]['ir_code'] += ['pop, ' + params[1]]
	p[0]['ir_code'] += p[2]['ir_code']
def p_function_header(p):
	"""function_header : LET IDENTIFIER parameter_list_or_empty EQUALS
	"""
	p[0] = ['int', p[2], p[3]]
	function_params = p[3]
	param_types = []
	param_num = 0
	if function_params != None:
		param_types = [param[0] for param in function_params]
		param_num = len(function_params)
	symbol_table.insert_function(p[2], 'int', param_types, param_num)

def p_parameter_list_or_empty(p):
	"""parameter_list_or_empty : empty
		| parameter_list
	"""
	p[0] = p[1]

def p_parameter_list(p):
	"""parameter_list : parameter
		| parameter_list  parameter
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1]) + [deepcopy(p[2])]

def p_parameter(p):
	"""parameter : type IDENTIFIER
	"""
	var = symbol_table.lookup(p[2], symbol_table.curr_table)
	if var != None:
		p[0] = [p[1],p[2]]
	else:
		print("ERROR MESSAGE: symbol '",p[2],"' used without declaration")
		print("COMPILATION HAS BEEN TERMINATED")
		exit()

def p_function_body(p):
	"""function_body : block ENDFUNCTION
	"""
	p[0] = deepcopy(p[1])

def p_return_statement(p):
	""" return_statement : RETURN expression ENDCOLON
	"""
	p[0] = {}
	p[0]['ir_code'] = [""]
	p[0]['value']: None
	p[0]['ir_code'] += p[2]['ir_code']
	p[0]['ir_code'] += ['return, ' + p[2]['value']]
def p_begin_scope(p):
	"""begin_scope : empty
	"""
	p[0] = p[1]
	symbol_table.begin_scope()

def p_empty(p):
	"""empty :"""
	pass



# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)

# Building the parser
parser = yacc.yacc(start='compilation_unit', debug=True, optimize=False)

# Read the input program
inputfile = open(filename, 'r')
data = inputfile.read()
result = parser.parse(data, debug=0)
