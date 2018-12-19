registersList = ['%eax', '%ebx', '%ecx', '%edx']                # Defining the list of register <= 6 in x86.

mathops = ['+', '-', '*', '/', 'mod']                           # Mathematical Operators in TAC.
tackeywords = ['goto', 'ifgoto', 'call', 'label', 'return', 'print','==', '<>', '<-', '>=', '<=', 'function', 'exit'] + mathops # TAC keywords used.

assembly = ""					                                # stream of Assembly code which will be generated.
registers = {}
registers = registers.fromkeys(registersList)                    # Constructing the register descriptor table.
# print(registers)

var_list = []				                                   	# Contains list of variables.
adrs_dscrptr = {}			                                     # Address descriptor table

next_use_table = []			                                     # Table for obtaining the next_use of a variable.

op_count = 1
