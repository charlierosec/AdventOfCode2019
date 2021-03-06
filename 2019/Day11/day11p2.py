#!/usr/bin/python3
#
# Advent of Code 2019
# Day 11 : Space Police
# 
# Author : Charlie Rose
# Language : Python3
# Date : 12/19/2019

################################# FUNCTIONS ###################################

def getOperand(op, mode):
    if mode == 2:
        # Relative Mode
        rv = accessMemory(op + relativeBase)
    elif mode == 1:
        # Immidiate Mode
        rv =  op
    elif mode == 0:
        # Destination Mode
        rv =  accessMemory(op)

    else:
        print( "Bad Mode" )
        return -1
    
    return rv

def increaseMemory(mem):
    global program
    while len(program) <= mem:
        program.append(0)

def accessMemory(loc):
    if loc >= len(program):
        increaseMemory(loc)
    return program[loc]

def editMemory(loc, val):
    global program
    if loc >= len(program):
        increaseMemory(loc)
    program[loc] = val

def changeBotFace(bf, dc):
    #dc 0 = L, 1 = R
    #bf 0 = N, 1 = E, 2 = S, 3 = W
    if bf == 0:
        if dc:
            return 1
        else:
            return 3
    elif bf == 1:
        if dc:
            return 2
        else:
            return 0
    elif bf == 2:
        if dc:
            return 3
        else:
            return 1 
    else:
        if dc:
            return 0
        else:
            return 2
 

##################################### MAIN ####################################

relativeBase = 0

# Robot Variables
tileColor = {}
  # 0 : Black
  # 1 : White
tilesPainted = 0
outputType = True
  # T : Color Tile Output
  # F : Turn Left or Right Output 
botLoc = (0,0)
botFacing = 0
  # 0 : North
  # 1 : East
  # 2 : South
  # 3 : West

#First tile is white
tileColor[botLoc] = 1

#For display purposes
maxX = 0
minX = 0
maxY = 0
minY = 0


# read the file and prep it for parsing
f = open("day11input.txt")
program = f.readlines()[0].split(",")
for i in range(0, len(program)):
    program[i] = int(program[i])


# do program
i = 0
while i < len(program):
    if accessMemory(i) > 99:
        longopcode = str(accessMemory(i))

        while len(longopcode) < 5:
            longopcode = "0" + longopcode

        opcode = int(longopcode[3:5])
        param1mode = int(longopcode[2])
        param2mode = int(longopcode[1])
        param3mode = int(longopcode[0])

    else:
        opcode = accessMemory(i)
        param1mode = 0
        param2mode = 0
        param3mode = 0

    # Opcode 1 : Add
    if opcode == 1:
        operand1 = accessMemory(i + 1)
        operand2 = accessMemory(i + 2)
        operand3 = accessMemory(i + 3)

        val1 = getOperand(operand1, param1mode)
        val2 = getOperand(operand2, param2mode)
        dest = operand3

        if param3mode == 2:
            dest += relativeBase

        editMemory(dest, val1 + val2)

        i += 4

    # Opcode 2 : Multiply
    if opcode == 2:
        operand1 = accessMemory(i + 1)
        operand2 = accessMemory(i + 2)
        operand3 = accessMemory(i + 3)
 
        val1 = getOperand(operand1, param1mode)
        val2 = getOperand(operand2, param2mode)
        dest = operand3

        if param3mode == 2:
            dest += relativeBase

        editMemory(dest, val1 * val2) 
            
        i += 4

########################## MAIN DAY 11 ALTERATIONS ############################
    # Opcode 3 : Get Input
    if opcode == 3:
        operand1 = accessMemory(i + 1)

        dest = operand1
        if param1mode == 2:
            dest += relativeBase

        if botLoc in tileColor.keys():
            value = tileColor[botLoc]
        else:
            value = 0

        editMemory(dest, value)
    
        i += 2 
    
    # Opcode 4 : Give Output
    if opcode == 4:
        operand1 = accessMemory(i + 1)
  
        outVal = getOperand(operand1, param1mode)

        if outputType:
            # T : Change Tile Color
            tileColor[botLoc] = outVal
        else:
            # F : Change Bot Facing
            botFacing = changeBotFace(botFacing, outVal)
            if botFacing == 0:
                botLoc = (botLoc[0], botLoc[1] + 1)
                if botLoc[1] > maxY:
                    maxY = botLoc[1]
            elif botFacing == 1:
                botLoc = (botLoc[0] + 1, botLoc[1])
                if botLoc[0] > maxX:
                    maxX = botLoc[0]
            elif botFacing == 2:
                botLoc = (botLoc[0], botLoc[1] - 1)
                if botLoc[1] < minY:
                    minY = botLoc[1]
            else:
                botLoc = (botLoc[0] - 1, botLoc[1])
                if botLoc[0] < minX:
                    minX = botLoc[0]
        
        outputType = not outputType

        i += 2
################################################################################

    # Opcode 5 : Jump If True
    if opcode == 5:
        operand1 = accessMemory(i + 1)
        operand2 = accessMemory(i + 2)
 
        test = getOperand(operand1, param1mode)
        dest = getOperand(operand2, param2mode)

        if test:
            i = dest
        else:
            i += 3

    # Opcode 6 : Jump If False
    if opcode == 6:
        operand1 = accessMemory(i + 1)
        operand2 = accessMemory(i + 2)
        
        test = getOperand(operand1, param1mode)
        dest = getOperand(operand2, param2mode)
            
        if (not test):
            i = dest
        else:
            i += 3

    # Opcode 7 : Less Than
    if opcode == 7:
        operand1 = accessMemory(i + 1)
        operand2 = accessMemory(i + 2)
        operand3 = accessMemory(i + 3)

        val1 = getOperand(operand1, param1mode)
        val2 = getOperand(operand2, param2mode)
        dest = operand3

        if param3mode == 2:
            dest += relativeBase

        editMemory(dest, int( val1 < val2 ))

        i += 4
            

    # Opcode 8 : Equals
    if opcode == 8:
        operand1 = accessMemory(i + 1)
        operand2 = accessMemory(i + 2)
        operand3 = accessMemory(i + 3)
        
        val1 = getOperand(operand1, param1mode)
        val2 = getOperand(operand2, param2mode)
        dest = operand3

        if param3mode == 2:
            dest += relativeBase

        editMemory(dest, int( val1 == val2 ))

        i += 4

    # Opcode 9 : Adjust Relative Base
    if opcode == 9:
        operand1 = accessMemory(i + 1)

        val1 = getOperand(operand1, param1mode)

        relativeBase += val1

        i += 2


    # Opcode 99 : Halt
    if opcode == 99:
        break

##################################### OUTPUT ##################################
w = abs(minX) + abs(maxX) + 1
h = abs(minY) + abs(maxY) + 1

output = ["."] * (w * h)

for c in tileColor.keys():
    cX = c[0]
    cY = abs(c[1])
    i = (cY * w) + cX

    if tileColor[c] == 1:
        output[i] = "#"
    else:
        output[i] = "."

for i in range(len(output)):
    print(output[i], end="")
    if (i%w) == 0:
        print()

print()
f.close()
