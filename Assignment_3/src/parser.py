
import sys
import ply.yacc as yacc
from lexer import *



if len(sys.argv) == 2:
	filename = sys.argv[1]
else:
	print("Usage: ./parser file.cs")
	exit(0)



################################################################################
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
def p_type_name(p):
	"""type_name : IDENTIFIER
	"""




# OC.2.2 Types
def p_type(p):
	"""type : INT
	"""


# OC.2.3 Expressions

def p_primary_expression(p):
	"""primary_expression : parenthesized_expression
		| literal
	"""
def p_parenthesized_expression(p):
	"""parenthesized_expression : LPAREN expression RPAREN
	"""
def p_literal(p):
	"""literal : NUM
				| CHAR_LITERAL
				| STRING_LITERAL
	"""
def p_function_call_paren(p):
	"""function_call_paren : LPAREN  function_call RPAREN
	"""
def p_function_call(p):
	"""function_call : called_function_name called_function_parameters
	"""
def p_called_function_name(p):
	"""called_function_name : IDENTIFIER
	"""
def p_called_function_parameters(p):
	"""called_function_parameters : called_function_parameters called_function_parameter
				| called_function_parameter
	"""
def p_called_function_parameter(p):
	"""called_function_parameter : IDENTIFIER
		| NUM
	"""
def p_post_increment_expression(p):
	"""post_increment_expression : postfix_expression PLUSPLUS
	"""
def p_post_decrement_expression(p):
	"""post_decrement_expression : postfix_expression MINUSMINUS
	"""

def p_postfix_expression(p):
	"""postfix_expression : function_call_paren
		| primary_expression
		| post_increment_expression
		| post_decrement_expression
		| IDENTIFIER
	"""
def p_unary_expression_not_plusminus(p):
	"""unary_expression_not_plusminus : postfix_expression
		| LNOT unary_expression
		| NOT unary_expression
	"""
def p_unary_expression(p):
	"""unary_expression : unary_expression_not_plusminus
		| PLUS unary_expression
		| MINUS unary_expression
		| MULT unary_expression

	"""
def p_multiplicative_expression(p):
	"""multiplicative_expression : unary_expression
		| multiplicative_expression MULT unary_expression
		| multiplicative_expression DIVIDE unary_expression
		| multiplicative_expression MOD unary_expression
	"""
def p_additive_expression(p):
	"""additive_expression : multiplicative_expression
		| additive_expression PLUS multiplicative_expression
		| additive_expression MINUS multiplicative_expression
	"""
def p_relational_expression(p):
	"""relational_expression : additive_expression
		| relational_expression LT additive_expression
		| relational_expression GT additive_expression
		| relational_expression LTEQ additive_expression
		| relational_expression GTEQ additive_expression
	"""
def p_equality_expression(p):
	"""equality_expression : relational_expression
		| equality_expression EQ relational_expression
		| equality_expression NE relational_expression
	"""
def p_conditional_and_expression(p):
	"""conditional_and_expression : equality_expression
		| conditional_and_expression AND equality_expression
	"""
def p_conditional_or_expression(p):
	"""conditional_or_expression : conditional_and_expression
		| conditional_or_expression OR conditional_and_expression
	"""
def p_assignment(p):
	"""assignment : unary_expression assignment_operator expression
	"""
def p_assignment_operator(p):
	"""assignment_operator : ASSIGN
							| EQUALS
	"""
def p_expression(p):
	"""expression : conditional_or_expression
		| assignment
	"""
def p_boolean_expression(p):
	"""boolean_expression : expression
		| TRUE
		| FALSE
	"""



# OC.2.4 Statements
def p_statement(p):
	"""statement : declaration_statement
		| embedded_statement
		| print_statement
	"""
def p_print_statement(p):
	"""print_statement : PRINT_INT LPAREN expression RPAREN ENDCOLON
		| PRINT_STR LPAREN STRING_LITERAL RPAREN ENDCOLON
	"""
def p_embedded_statement(p):
	"""embedded_statement : block
		| expression_statement
		| selection_statement
		| iteration_statement
	"""
def p_block(p):
	"""block : BEGIN statement_list_opt END
	"""
def p_statement_list_opt(p):
	"""statement_list_opt : empty
		| statement_list
	"""

def p_statement_list(p):
	"""statement_list : statement stmt_terminator_opt
		| statement_list statement stmt_terminator_opt
	"""

def p_stmt_terminator_opt(p):
	"""stmt_terminator_opt : ENDCOLON
		| empty
	"""
def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration
	"""
def p_global_variable_declaration(p):
	"""global_variable_declaration : LET variable_declarators IN
	"""
def p_local_variable_declaration(p):
	"""local_variable_declaration : LET variable_declarators IN
	"""
def p_variable_declarators(p):
	"""variable_declarators : type variable_declarator
		| variable_declarators type variable_declarator
	"""
def p_variable_declarator(p):
	"""variable_declarator : IDENTIFIER
		| IDENTIFIER assignment_operator variable_initializer
	"""
def p_variable_initializer(p):
	"""variable_initializer :  expression
	"""
def p_expression_statement(p):
	"""expression_statement : statement_expression
	"""
def p_statement_expression(p):
	"""statement_expression : empty
		| assignment
		| post_increment_expression
		| post_decrement_expression
	"""
def p_selection_statement(p):
	"""selection_statement : if_statement
	"""
def p_if_statement(p):
	"""if_statement : IF boolean_expression THEN statement
		| IF boolean_expression THEN statement ELSE statement
	"""
def p_iteration_statement(p):
	"""iteration_statement : while_statement
		| for_statement
	"""
def p_while_statement(p):
	"""while_statement : WHILE  boolean_expression  DO statement DONE
	"""
def p_for_statement(p):
	"""for_statement : FOR IDENTIFIER EQUALS ident1 upto_downto ident1  DO statement DONE
	"""
def p_ident1(p):
	"""ident1 : NUM
		| IDENTIFIER
	"""
def p_upto_downto(p):
	"""upto_downto : UPTO
		| DOWNTO
	"""




# OC.2.5 Compilation Unit

def p_module(p):
	"""module : open_directives_opt
		| open_directives_opt module_member_declarations
	"""
def p_open_directives_opt(p):
	"""open_directives_opt : empty
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
def p_module_member_declarations(p):
	"""module_member_declarations : module_member_declaration
		| module_member_declarations module_member_declaration
	"""

def p_module_member_declaration(p):
	"""module_member_declaration : module_member_type_declaration
	"""
def p_module_member_type_declaration(p):
	"""module_member_type_declaration : function_declaration
		| global_variable_declaration
	"""




# OC.2.6 functions


def p_function_declaration(p):
	"""function_declaration : function_header function_body
	"""

def p_function_header(p):
	"""function_header : LET IDENTIFIER parameter_list_opt EQUALS

	"""
def p_parameter_list_opt(p):
	"""parameter_list_opt : empty
		| parameter_list
	"""
def p_parameter_list(p):
	"""parameter_list : parameter
		| parameter_list  parameter
	"""
def p_parameter(p):
	"""parameter : type IDENTIFIER
	"""
def p_function_body(p):
	"""function_body : statement return_value ENDFUNCTION

	"""
def p_return_value(p):
	""" return_value : RETURN expression stmt_terminator_opt
		| empty
	"""

def p_empty(p):
	"""empty :"""
	pass



# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)

# Building the parser
parser = yacc.yacc(start='module', debug=True, optimize=False)

# Read the input program
inputfile = open(filename, 'r')
data = inputfile.read()
result = parser.parse(data, debug=2)
