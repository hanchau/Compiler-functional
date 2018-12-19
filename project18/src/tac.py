def print_tac(p):
#	print("IR Code")
#	print("")
#	print("1, call, Main")
#	print("2, exit")
	temp = 1
	for i in p:
		for line in i['ir_code']:
			if line != "":
				print(str(temp) + ", " + line)
				temp = temp + 1
