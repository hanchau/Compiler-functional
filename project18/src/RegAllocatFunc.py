import sys
import GlobalVariables as GV


def isNum(num):
    num=str(num).strip(' ')
    if(num[0]=='-'):
        num=num[1:]
        return num.isdigit()
    else:
        return num.isdigit()



def getReg(variable, instrno):                  #getReg for returning register for variable.
	if variable in GV.registers.values():
		for x in GV.registers.keys():
			if GV.registers[x] == variable:
				return x
	for var in GV.registers.keys():
		if GV.registers[var] == None:
			return var
	instrvardict = GV.next_use_table[instrno - 1]
	nextUseFar = max(instrvardict.keys())
	for var in instrvardict:
		if instrvardict[var] == nextUseFar:
			break;
	for reg_spill in GV.registers.keys():
		if GV.registers[reg_spill] == var:
			break;
	GV.assembly = GV.assembly + "movl " + reg_spill + ", " + var + "\n"

	return reg_spill


def getLoc(variable):
    loctn = GV.adrs_dscrptr[variable]
    return loctn


def setReg(register, content):     # for setting the register descriptor entry based on the args
    reg = register
    cont = content
    GV.registers[reg] = cont


def setLoc(variable, location):     #for setting the location of variable in address descriptor tabe
    var = variable
    loctn = location
    GV.adrs_dscrptr[var] = loctn
