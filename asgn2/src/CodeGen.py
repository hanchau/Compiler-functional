#!/usr/bin/python3

import sys
import GlobalVariables as GV
import RegAllocatFunc as RAF
import TransInstr as TR

if len(sys.argv) == 2:
	_file = str(sys.argv[1])
else:
	print("argv[0] = codegen.py and argv[1] = ir_testfile")
	exit()



test_file = open(_file, 'r')
test_file = test_file.read()


list_instr = []								# defining the list of instruction.
list_instr = (test_file.strip("\n")).split('\n')

len_list = len(list_instr)
#print(range(len(list_instr))

for instr in list_instr:					# Making the instr list and address Descriptor Table.
	templist = instr.split(', ')
	if templist[1] not in ['label', 'call', 'function']:
		GV.var_list = GV.var_list + templist


GV.var_list = list(set(GV.var_list))

GV.var_list = [x for x in GV.var_list if not RAF.isNum(x)]

for keyword in GV.tackeywords:
	if keyword in GV.var_list:
		GV.var_list.remove(keyword)


GV.adrs_dscrptr = GV.adrs_dscrptr.fromkeys(GV.var_list, "mem")
symbol_table = GV.adrs_dscrptr.fromkeys(GV.var_list, ["live", None])

leaders = [1,]
for k in range(len(list_instr)):
	list_instr[k] = list_instr[k].split(', ')
	if 'ifgoto' in list_instr[k]:
		leaders.append(int(list_instr[k][-1]))
		#print(leaders)
		leaders.append(int(list_instr[k][0])+1)
	elif 'goto' in list_instr[k]:
		leaders.append(int(list_instr[k][-1]))
		#print(leaders)
		leaders.append(int(list_instr[k][0])+1)
	elif 'function' in list_instr[k]:
		leaders.append(int(list_instr[k][0]))
	elif 'label' in list_instr[k]:
		leaders.append(int(list_instr[k][0]))

leaders = list(set(leaders))
leaders.sort()
#print(leaders)

# Constructing the Basic Blocks as blocks
blocks = []
i = 0
while i < len(leaders)-1:
	blocks.append(list(range(leaders[i],leaders[i+1])))
	i = i + 1
blocks.append(list(range(leaders[i],len(list_instr)+1)))


GV.next_use_table = [None for i in range(len(list_instr))]	#defining empty
#print(GV.next_use_table)



for block in blocks:			# For nextuse Table.
	new_list = block.copy()
	new_list.reverse()

	for instr_line_no in new_list:
		instr = list_instr[instr_line_no - 1]
		operator = instr[1]
		variables = [var for var in instr if var in GV.var_list]
		GV.next_use_table[instr_line_no-1] = {var:symbol_table[var] for var in GV.var_list}


		if operator in GV.mathops:	# math operations
			var1 = instr[2]
			var2 = instr[3]
			var3 = instr[4]
			if var3 in variables:
				symbol_table[var3] = ["live", instr_line_no]
			if var2 in variables:
				symbol_table[var2] = ["live", instr_line_no]
			if var1 in variables:
				symbol_table[var1] = ["dead", None]


		elif operator == "ifgoto":
			var4 = instr[3]
			var5 = instr[4]
			if var4 in variables:
				symbol_table[var4] = ["live", instr_line_no]
			if var5 in variables:
				symbol_table[var5] = ["live", instr_line_no]


		elif operator == "<-":
			var6 = instr[2]
			var7 = instr[3]
			if var6 in variables:
				symbol_table[var6] = ["dead", None]
			if var7 in variables:
				symbol_table[var7] = ["live", instr_line_no]

		elif operator == "print":
			x = instr[2]
			if x in variables:
				symbol_table[x] = ["live", instr_line_no]

		i = i - 1




for var in GV.var_list:
	data_section = ".section .data\n" + var + ":\t" + ".int 0\n"
data_section = "\n" + data_section + "str:.ascii \"%d\\n\\0\"\n"

bss_section = ".section  .bss\n"
text_section = ".section .text\n" + ".globl main\n" + "main:\n"



for block in blocks:
	text_section = text_section + "L" + str(block[0]) + ":\n"
	for block in block:
		text_section = text_section + TR.translate(list_instr[block - 1])


print(data_section + bss_section + text_section)		#x86 would be combined all togather.
