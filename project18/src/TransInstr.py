import sys
import GlobalVariables as GV
import RegAllocatFunc as RAF


#Translating single instruction line into X86 code.
def translate(instr):

	oprtr = instr[1]
	line = int(instr[0])
	GV.assembly = ""

	if oprtr in GV.mathops:				# Assembly code for TAC being math op
		oprtn_rslt = instr[2]
		oprnd1 = instr[4]
		oprnd2 = instr[3]

		if oprtr == '-':					# Assembly code for Subtraction operator.
			if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				GV.assembly = GV.assembly + "movl $" + str(int(oprnd2)-int(oprnd1)) + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, oprtn_rslt)					# now updating address descriptor entry for result variable.
				RAF.setLoc(oprtn_rslt, destn_regstr)
			elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				loctn2 = RAF.getLoc(oprnd2)

				if loctn2 != "mem":											# moving operand1 to destination register.
					GV.assembly = GV.assembly + "movl " + loctn2 + ", " + destn_regstr + "\n"
				else:
					GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "subl $" + oprnd1 + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, oprtn_rslt)
				RAF.setLoc(oprtn_rslt, destn_regstr)
			elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				loctn1 = RAF.getLoc(oprnd1)
				GV.assembly = GV.assembly + "movl $" + oprnd2 + ", " + destn_regstr + "\n"	# moving operand1 to destination register.
				if loctn1 != "mem":											# Adding operand 2 to the register
					GV.assembly = GV.assembly + "subl " + loctn1 + ", " + destn_regstr + "\n"
				else:
					GV.assembly = GV.assembly + "subl " + oprnd1 + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, oprtn_rslt)
				RAF.setLoc(oprtn_rslt, destn_regstr)
			elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				loctn1 = RAF.getLoc(oprnd1)							# getting location
				loctn2 = RAF.getLoc(oprnd2)							# of the operands
				if loctn1 != "mem" and loctn2 != "mem":
					GV.assembly = GV.assembly + "movl " + loctn2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "subl " + loctn1 + ", " + destn_regstr + "\n"
				elif loctn1 == "mem" and loctn2 != "mem":
					GV.assembly = GV.assembly + "movl " + loctn2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "subl " + oprnd1 + ", " + destn_regstr + "\n"
				elif loctn1 != "mem" and loctn2 == "mem":
					GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "subl " + loctn1 + ", " + destn_regstr + "\n"
				elif loctn1 == "mem" and loctn2 == "mem":
					GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "subl " + oprnd1 + ", " + destn_regstr + "\n"

				RAF.setReg(destn_regstr, oprtn_rslt)					# setting register descriptor for destn_regstr
				RAF.setLoc(oprtn_rslt, destn_regstr)					# setting address deescriptor for oprtn_rslt.

		elif oprtr == '+':					# Assembly code for addition operator.
			if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				GV.assembly = GV.assembly + "movl $" + str(int(oprnd2)+int(oprnd1)) + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, oprtn_rslt)					# now updating address descriptor entry for result variable.
				RAF.setLoc(oprtn_rslt, destn_regstr)
			elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				loctn2 = RAF.getLoc(oprnd2)
				GV.assembly = GV.assembly + "movl $" + oprnd1 + ", " + destn_regstr + "\n"
				if loctn2 != "mem":											# moving operand1 to destination register.
					GV.assembly = GV.assembly + "addl " + loctn2 + ", " + destn_regstr + "\n"
				else:
					GV.assembly = GV.assembly + "addl " + oprnd2 + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, oprtn_rslt)
				RAF.setLoc(oprtn_rslt, destn_regstr)
			elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				loctn1 = RAF.getLoc(oprnd1)
				GV.assembly = GV.assembly + "movl $" + oprnd2 + ", " + destn_regstr + "\n"	# moving operand1 to destination register.
				if loctn1 != "mem":											# Adding operand 2 to the register
					GV.assembly = GV.assembly + "addl " + loctn1 + ", " + destn_regstr + "\n"
				else:
					GV.assembly = GV.assembly + "addl " + oprnd1 + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, oprtn_rslt)
				RAF.setLoc(oprtn_rslt, destn_regstr)
			elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				destn_regstr = RAF.getReg(oprtn_rslt, line)					# getting register to store the result of operation
				loctn1 = RAF.getLoc(oprnd1)							# getting location
				loctn2 = RAF.getLoc(oprnd2)							# of the operands
				if loctn1 != "mem" and loctn2 != "mem":
					GV.assembly = GV.assembly + "movl " + loctn2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "addl " + loctn1 + ", " + destn_regstr + "\n"
				elif loctn1 == "mem" and loctn2 != "mem":
					GV.assembly = GV.assembly + "movl " + loctn2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "addl " + oprnd1 + ", " + destn_regstr + "\n"
				elif loctn1 != "mem" and loctn2 == "mem":
					GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "addl " + loctn1 + ", " + destn_regstr + "\n"
				elif loctn1 == "mem" and loctn2 == "mem":
					GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
					GV.assembly = GV.assembly + "addl " + oprnd1 + ", " + destn_regstr + "\n"

				RAF.setReg(destn_regstr, oprtn_rslt)					# setting register descriptor for destn_regstr
				RAF.setLoc(oprtn_rslt, destn_regstr)					# setting address deescriptor for oprtn_rslt.

		elif oprtr == '/':					# Assembly code for division operator.
			if GV.registers['%eax'] != None:
				GV.assembly = GV.assembly + "movl %eax, " + GV.registers['%eax'] + "\n"
				RAF.setLoc(GV.registers['%eax'], "mem")

			if GV.registers['%edx'] != None:
				GV.assembly = GV.assembly + "movl %edx, " + GV.registers['%edx'] + "\n"
				RAF.setLoc(GV.registers['%edx'], "mem")

			if GV.registers['%ecx'] != None:
				GV.assembly = GV.assembly + "movl %ecx, " + GV.registers['%ecx'] + "\n"
				RAF.setLoc(GV.registers['%ecx'], "mem")

			if not RAF.isNum(oprnd1):
				loctn1 = RAF.getLoc(oprnd1)
				RAF.setLoc(oprnd1, "mem")

			if not RAF.isNum(oprnd2):
				loctn2 = RAF.getLoc(oprnd2)
				RAF.setLoc(oprnd2, "mem")
			GV.assembly = GV.assembly + "movl $0, %edx \n"

			if not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", %eax \n"
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", %ecx \n"
				GV.assembly = GV.assembly + "idiv %ecx \n"
				RAF.setLoc(oprtn_rslt, '%eax')

			elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				GV.assembly = GV.assembly + "movl $" + (oprnd1) + ", %eax \n"
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", %ecx \n"
				GV.assembly = GV.assembly + "idiv %ecx \n"
				RAF.setLoc(oprtn_rslt, '%eax')

			elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
				loctn1 = RAF.getLoc(oprnd1)
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", %eax \n"
				GV.assembly = GV.assembly + "movl $" + (oprnd2) + ", %ecx \n"
				GV.assembly = GV.assembly + "idiv %ecx \n"
				RAF.setLoc(oprtn_rslt, '%eax')

			else:
				ansdiv = int(int(oprnd1)/int(oprnd2))
				GV.assembly = GV.assembly + "movl $" + str(ansdiv) + ", %eax \n"
				RAF.setLoc(oprtn_rslt, '%eax')

		elif oprtr == '*':					# Assembly code for Multiplication operator.
			if GV.registers['%eax'] != None:
					GV.assembly = GV.assembly + "movl %eax, " + GV.registers['%eax'] + "\n"
					RAF.setLoc(GV.registers['%eax'], "mem")
			if GV.registers['%edx'] != None:

					GV.assembly = GV.assembly + "movl %edx, " + GV.registers['%edx'] + "\n"
					RAF.setLoc(GV.registers['%edx'], "mem")

			if not RAF.isNum(oprnd1):
				loctn1 = RAF.getLoc(oprnd1)
				RAF.setLoc(oprnd1, "mem")

			if not RAF.isNum(oprnd2):
				loctn2 = RAF.getLoc(oprnd2)
				RAF.setLoc(oprnd2, "mem")

			if not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", %eax \n"
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", %edx \n"
				GV.assembly = GV.assembly + "imul %edx \n"
				RAF.setLoc(oprtn_rslt, '%eax')

			elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				GV.assembly = GV.assembly + "movl $" + (oprnd1) + ", %eax \n"
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", %edx \n"
				GV.assembly = GV.assembly + "imul %edx \n"
				RAF.setLoc(oprtn_rslt, '%eax')

			elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", %eax \n"
				GV.assembly = GV.assembly + "movl $" + (oprnd2) + ", %edx \n"
				GV.assembly = GV.assembly + "imul %edx \n"
				RAF.setLoc(oprtn_rslt, '%eax')

			else:
				ansmul = int(oprnd1)*int(oprnd2)
				GV.assembly = GV.assembly + "movl $" + str(ansmul) + ", %eax \n"
				RAF.setLoc(oprtn_rslt, '%eax')



	elif oprtr == "and":					# Assembly code for TAC being logical AND op (LINENO, &&, RESULT, OPRND1, OPRND2)
		oprtn_rslt = instr[2]
		oprnd1 = instr[3]
		oprnd2 = instr[4]
		if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			GV.assembly = GV.assembly + "movl $" + str(int(oprnd1) and int(oprnd2)) + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn2 = RAF.getLoc(oprnd2)
			GV.assembly = GV.assembly + "movl $" + oprnd1 + ", " + destn_regstr + "\n"
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "and " + loctn2 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "and " + oprnd2 + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "and $" + oprnd2 + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			loctn2 = RAF.getLoc(oprnd2)
			if loctn1 != "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "and " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "and " + oprnd2 + ", " + destn_regstr + "\n"
			elif loctn1 != "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "and " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "and " + oprnd2 + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)

	elif oprtr == "or":					# Assembly code for TAC being logical OR op (LINENO, ||, RESULT, OPRND1, OPRND2)
		oprtn_rslt = instr[2]
		oprnd1 = instr[3]
		oprnd2 = instr[4]
		if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			GV.assembly = GV.assembly + "movl $" + str(int(oprnd1) or int(oprnd2)) + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn2 = RAF.getLoc(oprnd2)
			GV.assembly = GV.assembly + "movl $" + oprnd1 + ", " + destn_regstr + "\n"
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "or " + loctn2 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "or " + oprnd2 + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "or $" + oprnd2 + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			loctn2 = RAF.getLoc(oprnd2)
			if loctn1 != "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "or " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "or " + oprnd2 + ", " + destn_regstr + "\n"
			elif loctn1 != "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "or " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "or " + oprnd2 + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)

	elif oprtr == '<=':					# Assembly code for TAC being LTE op (LINENO, IFGOTO, <=, OPRND1, OPRND2, LINENO_TO_GO_TO)
		oprtn_rslt = instr[2]
		oprnd1 = instr[3]
		oprnd2 = instr[4]
		LT = "LT"+str(GV.op_count)
		NLT = "NLT"+str(GV.op_count)
		if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):

			destn_regstr = RAF.getReg(oprtn_rslt, line)
			GV.assembly = GV.assembly + "movl $" + str(int(int(oprnd1)<=int(oprnd2))) + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn2 = RAF.getLoc(oprnd2)
			GV.assembly = GV.assembly + "movl $" + oprnd1 + ", " + destn_regstr + "\n"
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd2 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jle " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			GV.assembly = GV.assembly + "movl $" + oprnd2 + ", " + destn_regstr + "\n"
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jle " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			loctn2 = RAF.getLoc(oprnd2)
			if loctn1 != "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 != "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jle " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		GV.op_count = GV.op_count + 1

	elif oprtr == '>=':					# Assembly code for TAC being GTE op (LINENO, IFGOTO, >=, OPRND1, OPRND2, LINENO_TO_GO_TO)
		oprtn_rslt = instr[2]
		oprnd1 = instr[3]
		oprnd2 = instr[4]
		LT = "LT"+str(GV.op_count)
		NLT = "NLT"+str(GV.op_count)
		if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			GV.assembly = GV.assembly + "movl $" + str(int(int(oprnd1)>=int(oprnd2))) + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn2 = RAF.getLoc(oprnd2)
			GV.assembly = GV.assembly + "movl $" + oprnd1 + ", " + destn_regstr + "\n"
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd2 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jge " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			GV.assembly = GV.assembly + "movl $" + oprnd2 + ", " + destn_regstr + "\n"
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jge " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			loctn2 = RAF.getLoc(oprnd2)
			if loctn1 != "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 != "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jge " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		GV.op_count = GV.op_count + 1

	elif oprtr == '==':					# Assembly code for TAC being Comparison op (LINENO, IFGOTO, == , OPRND1, OPRND2, LINENO_TO_GO_TO)
		oprtn_rslt = instr[2]
		oprnd1 = instr[3]
		oprnd2 = instr[4]
		LT = "LT"+str(GV.op_count)
		NLT = "NLT"+str(GV.op_count)
		if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			GV.assembly = GV.assembly + "movl $" + str(int(int(oprnd1)==int(oprnd2))) + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn2 = RAF.getLoc(oprnd2)
			GV.assembly = GV.assembly + "movl $" + oprnd1 + ", " + destn_regstr + "\n"
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd2 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "je " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			GV.assembly = GV.assembly + "movl $" + oprnd2 + ", " + destn_regstr + "\n"
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "je " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			loctn2 = RAF.getLoc(oprnd2)
			if loctn1 != "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 != "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "je " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		GV.op_count = GV.op_count + 1

	elif oprtr == '!=':					# Assembly code for TAC being NE op (LINENO, IFGOTO, <>, OPRND1, OPRND2, LINENO_TO_GO_TO)
		oprtn_rslt = instr[2]
		oprnd1 = instr[3]
		oprnd2 = instr[4]
		LT = "LT"+str(GV.op_count)
		NLT = "NLT"+str(GV.op_count)
		if RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			GV.assembly = GV.assembly + "movl $" + str(int(int(oprnd1)!=int(oprnd2))) + ", " + destn_regstr + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn2 = RAF.getLoc(oprnd2)
			GV.assembly = GV.assembly + "movl $" + oprnd1 + ", " + destn_regstr + "\n"
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd2 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jne " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			GV.assembly = GV.assembly + "movl $" + oprnd2 + ", " + destn_regstr + "\n"
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			else:
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jne " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		elif not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			destn_regstr = RAF.getReg(oprtn_rslt, line)
			loctn1 = RAF.getLoc(oprnd1)
			loctn2 = RAF.getLoc(oprnd2)
			if loctn1 != "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn2 + ", " + destn_regstr + "\n"
			elif loctn1 != "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + loctn1 + ", " + destn_regstr + "\n"
			elif loctn1 == "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", " + destn_regstr + "\n"
				GV.assembly = GV.assembly + "cmpl " + oprnd1 + ", " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jne " + LT + "\n"
			GV.assembly = GV.assembly + "movl $0, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + "jmp NLT" + "\n"
			GV.assembly = GV.assembly + LT + ":" + "\n"
			GV.assembly = GV.assembly + "movl $1, " + destn_regstr + "\n"
			GV.assembly = GV.assembly + NLT + ":" + "\n"
			RAF.setReg(destn_regstr, oprtn_rslt)
			RAF.setLoc(oprtn_rslt, destn_regstr)
		GV.op_count = GV.op_count + 1

	elif oprtr == '=':					# Assembly code for TAC being Assignment op (LINENO, <-, DEST_VAR, SRC_VAR)
		des_var = instr[2]
		src_var = instr[3]
		loctn1 = RAF.getLoc(des_var)
		if RAF.isNum(src_var):
			if loctn1 == "mem":
				GV.assembly = GV.assembly + "movl $" + src_var + ", " + des_var + "\n"
			else:
				GV.assembly = GV.assembly + "movl $" + src_var + ", " + loctn1 + "\n"
		else:
			loctn2 = RAF.getLoc(src_var)
			if loctn1 == "mem" and loctn2 == "mem":
				destn_regstr = RAF.getReg(des_var, line)
				GV.assembly = GV.assembly + "movl " + src_var + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, des_var)
				RAF.setLoc(des_var, destn_regstr)
			elif loctn1 == "mem" and loctn2 != "mem":
				destn_regstr = RAF.getReg(des_var, line)
				GV.assembly = GV.assembly + "movl " + loctn2 + ", " + destn_regstr + "\n"
				RAF.setReg(destn_regstr, des_var)
				RAF.setLoc(des_var, destn_regstr)
			elif loctn1 != "mem" and loctn2 == "mem":
				GV.assembly = GV.assembly + "movl " + src_var + ", " + loctn1 + "\n"
			elif loctn1 != "mem" and loctn2 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn2 + ", " + loctn1 + "\n"



	elif oprtr == 'mod':				# Assembly code for TAC being modulus(LIKE MATH OPERATORS)
			if GV.registers['%eax'] != None:
				GV.assembly = GV.assembly + "movl %eax, " + GV.registers['%eax'] + "\n"
				RAF.setLoc(GV.registers['eax'], "mem")
			if GV.registers['%edx'] != None:
				GV.assembly = GV.assembly + "movl %edx, " + GV.registers['%edx'] + "\n"
				RAF.setLoc(GV.registers['%edx'], "mem")
			if GV.registers['%ecx'] != None:
				GV.assembly = GV.assembly + "movl %ecx, " + GV.registers['%ecx'] + "\n"
				RAF.setLoc(GV.registers['%ecx'], "mem")
			if not RAF.isNum(oprnd1):
				loctn1 = RAF.getLoc(oprnd1)
				RAF.setLoc(oprnd1, "mem")
			if not RAF.isNum(oprnd2):
				loctn2 = RAF.getLoc(oprnd2)
				RAF.setLoc(oprnd2, "mem")
			GV.assembly = GV.assembly + "movl $0, %edx \n"
			if not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", %eax \n"
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", %ecx \n"
				GV.assembly = GV.assembly + "idiv %ecx \n"
				RAF.setLoc(oprtn_rslt, '%edx')
			elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
				GV.assembly = GV.assembly + "movl $" + oprnd1 + ", %eax \n"
				GV.assembly = GV.assembly + "movl " + oprnd2 + ", %ecx \n"
				GV.assembly = GV.assembly + "idiv %ex \n"
				RAF.setLoc(oprtn_rslt, '%edx')
			elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
				loctn1 = RAF.getLoc(oprnd1)
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", %eax \n"
				GV.assembly = GV.assembly + "movl $" + (oprnd2) + ", %ecx \n"
				GV.assembly = GV.assembly + "idiv %ecx \n"
				RAF.setLoc(oprtn_rslt, '%edx')
			else:
				ansmod = int(int(oprnd1)/int(oprnd2))
				GV.assembly = GV.assembly + "movl $" + str(ansmod) + ", %edx \n"
				RAF.setLoc(oprtn_rslt, '%edx')

	elif oprtr == "call":				# Assembly code for TAC being a function call (LINENO, CALL, <FUNCTION_NAME>, NUM_ARGS )
		arg_num = instr[3]
		for var in GV.var_list:
			loc = RAF.getLoc(var)
			if loc != "mem":
				GV.assembly = GV.assembly + "movl " + loc + ", " + var + "\n"
				RAF.setLoc(var, "mem")
		label = instr[2]
		GV.assembly = GV.assembly + "call " + label + "\n"

	elif oprtr == "label":				# Assembly code for TAC being Block (LINENO, LABEL, <LABEL_NAME>)
		label = instr[2]
		GV.assembly = GV.assembly + label + ": \n"

	elif oprtr == "ifgoto":				# Assembly code for TAC being ifgoto statement (LINENO, IFGOTO, CONDITION, OPRND1, OPRND2, LINENO_TO_GO_TO)
		for var in GV.var_list:
			loc = RAF.getLoc(var)
			if loc != "mem":
				GV.assembly = GV.assembly + "movl " + loc + ", " + var + "\n"
				RAF.setLoc(var, "mem")
		oprtr = instr[2]
		oprnd1 = instr[3]
		oprnd2 = instr[4]
		label = instr[5]
		if not RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			loctn1 = RAF.getLoc(oprnd1)
			loctn2 = RAF.getLoc(oprnd2)
			reg1 = RAF.getReg(oprnd1, line)
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "movl " + loctn1 + ", " + reg1 + "\n"
			else:
				GV.assembly = GV.assembly + "movl " + oprnd1 + ", " + reg1 + "\n"
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "cmp " + loctn2 + ", " + reg1 + "\n"
			else:
				GV.assembly = GV.assembly + "cmp " + oprnd2 + ", " + reg1 + "\n"
			RAF.setReg(reg1, oprnd1)
			RAF.setLoc(oprnd1, reg1)
		elif not RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			loctn1 = RAF.getLoc(oprnd1)
			if loctn1 != "mem":
				GV.assembly = GV.assembly + "cmp $" + oprnd2 + ", " + loctn1 + "\n"
			else:
				GV.assembly = GV.assembly + "cmp $" + oprnd2 + ", " + oprnd1 + "\n"
		elif RAF.isNum(oprnd1) and not RAF.isNum(oprnd2):
			loctn2 = RAF.getLoc(oprnd2)
			if loctn2 != "mem":
				GV.assembly = GV.assembly + "cmp " + loctn2 + ", $" + oprnd1 + "\n"
			else:
				GV.assembly = GV.assembly + "cmp " + oprnd2 + ", $" + oprnd1 + "\n"
		elif RAF.isNum(oprnd1) and RAF.isNum(oprnd2):
			GV.assembly = GV.assembly + "cmp $" + oprnd2 + ", $" + oprnd1 + "\n"
		for var in GV.var_list:
			loc = RAF.getLoc(var)
			if loc != "mem":
				GV.assembly = GV.assembly + "movl " + loc + ", " + var + "\n"
				RAF.setLoc(var, "mem")
		if RAF.isNum(label):
			label = "L" + label
		if oprtr == "<=":
			GV.assembly = GV.assembly + "jle " + label + "\n"
		elif oprtr == ">=":
			GV.assembly = GV.assembly + "jge " + label + "\n"
		elif oprtr == "==":
			GV.assembly = GV.assembly + "je " + label + "\n"
		elif oprtr == "!=":
			GV.assembly = GV.assembly + "jne " + label + "\n"

	elif oprtr == "goto":				# Assembly code for TAC being goto statement (LINENO, GOTO, LINENO_TO_GO_TO)
		for var in GV.var_list:
			loc = RAF.getLoc(var)
			if loc != "mem":
				GV.assembly = GV.assembly + "movl " + loc + ", " + var + "\n"
				RAF.setLoc(var, "mem")

		label = instr[2]
		if RAF.isNum(label):
			GV.assembly = GV.assembly + "jmp L" + label + "\n"
		else:
			GV.assembly = GV.assembly + "jmp " + label + "\n"

	elif oprtr == "exit":				# Assembly code for TAC being exit statement (LINENO, EXIT)
		GV.assembly = GV.assembly + "call exit\n"

	elif oprtr == "print":				# Assembly code for TAC being print statement (LINENO, PRINT, VAR_NAME)
		operand = instr[2]
		if not RAF.isNum(operand):
			loc = RAF.getLoc(operand)
			if not loc == "mem":
				GV.assembly = GV.assembly + "pushl " + loc + "\n"
				GV.assembly = GV.assembly + "pushl $str\n"
				GV.assembly = GV.assembly + "call printf\n"
			else:
				GV.assembly = GV.assembly + "pushl " + operand + "\n"
				GV.assembly = GV.assembly + "pushl $str\n"
				GV.assembly = GV.assembly + "call printf\n"
		else:
			GV.assembly = GV.assembly + "pushl $" + operand + "\n"
			GV.assembly = GV.assembly + "pushl $str\n"
			GV.assembly = GV.assembly + "call printf\n"

	elif oprtr == "function":			# Preclude for TAC being function (LINENO, FUNCTION, <FUNCTION_NAME>)
		function_name = instr[2]
		GV.assembly = GV.assembly + ".globl " + function_name + "\n"
		GV.assembly = GV.assembly + ".type "  + function_name + ", @function\n"
		GV.assembly = GV.assembly + function_name + ":\n"
		GV.assembly = GV.assembly + "pushl %ebp\n"
		GV.assembly = GV.assembly + "movl %esp, %ebp\n"

	elif oprtr == "arg":					# Assembly code for TAC being multiple args i.e it will shift param i to var a_i (LINENO, ARG, I, A_I)
		i = instr[2]
		a = instr[3]
		displace = 4*i + 4
		GV.assembly = GV.assembly + "movl " + str(displace) + "(%ebp), " + a + "\n"

	elif oprtr == "pop":				#for popping (LINENO, POP, N)
		n = instr[2]
		GV.assembly = GV.assembly + "addl $4, $esp\n"

	elif oprtr == "return":				# conclude for TAC being return (LINENO, RETURN, VALUE)
		val = instr[2]
		if RAF.isNum(val):
			val = "$" + val
		for var in GV.var_list:
			loc = RAF.getLoc(var)
			if loc == "%eax":
				GV.assembly = GV.assembly + "movl " + loc + ", " + var + "\n"
				RAF.setLoc(var, "mem")
				break
		GV.assembly = GV.assembly + "movl " + val + ", %eax\n"
		GV.assembly = GV.assembly + "movl %ebp, %esp\n"
		GV.assembly = GV.assembly + "popl %ebp\n"
		GV.assembly = GV.assembly + "ret\n"


	return GV.assembly
