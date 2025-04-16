from formatmaps import format1, format2,format3,format4,format4f
def pass2():
    symboltable={}
    literaltable={}
    startaddress={}
    baseaddress={}

    with open("symboltable.txt", "r") as symfile:
        symboltable = {line.split(":")[0]: int(line.split(":")[1], 16) for line in symfile}

    with open("literaltable.txt", "r") as litfile:
        literaltable = {line.split(":")[0]: int(line.split(":")[1], 16) for line in litfile}
    with open("INTERMEDIATE.txt", "r") as file:
        # Read all lines from the file
        lines = file.readlines()
    with open("blockstarting.txt", "r") as file2:
        # Read all lines from the file
        startaddress={line.split(":")[0]: int(line.split(":")[1], 16) for line in file2}
    with open("base.txt", "r") as file3:
        # Read all lines from the file
        baseaddress = {line.split(":")[0]: int(line.split(":")[1], 16) for line in file3}
    with open("output_pass2.txt", "w") as file4:
        file4.write("")
    registers = {
        "0":0x0,
        "A": 0x0,
        "X": 0x1,
        "L": 0x2,
        "B": 0x3,
        "S": 0x4,
        "T": 0x5,
        "F": 0x6,
        "PC": 0x8,
        "SW": 0x9
    }
    startlc=0
    endlc=0
    for line in lines:
        words = line.split()
        block, lc, *rest = words
        lc = int(lc, 16)+startaddress[block]
        lc2=hex(lc)
        s=""
        s+=block
        s+=" "
        s+=str(lc2)
        s+=" "
        #print(words)
        for i in range(len(rest)):
            if rest[i]=="START":
                s+=rest[i-1]
                startlc=lc
                break
            elif  rest[i]=="END":
                endlc=lc
                s+="END"
                break

            elif  rest[i] in format1:
                object_code = format1[rest[i]]
                s+=f"{object_code:02X}"
                break


            elif rest[i] in format2:

                opcode = format2[rest[i]]
                regs=rest[i+1:]
                regs="".join(regs)
                operands=regs.split(",")
                if(len(operands)>1):
                    reg1=registers[operands[0]]
                    reg2=registers[operands[1]]
                else :
                    reg1=registers[operands[0]]
                    reg2=0
                object_code = (opcode << 8) | (reg1 << 4) | reg2

                s+=f"{object_code:04X}"
                break

            elif rest[i] in format3:
                x=0
                e = 0
                inputs = rest[i + 1:]
                inputs = "".join(inputs)
                operands = inputs.split(",")
                if (len(operands) > 1):
                    x = 1
                    var = (operands[0])
                else:
                    x = 0
                    var = (operands[0])

                opcode = format3[rest[i]]
                #print(operands)
                if(var!=""):

                    n=0
                    i=0
                    if var[0]=='#':
                        n = 0
                        i = 1
                        var=var[1:]
                    elif var[0]=='@':
                        n = 1
                        i = 0
                        var=var[1:]
                    else:
                        n = 1
                        i = 1
                    displacement=0
                    if i and var.isdigit():
                        displacement=int(var)
                    elif(var in symboltable):
                        displacement = symboltable[var] - (lc + 3)
                    elif (var in literaltable):
                        displacement=literaltable[var]-(lc+3)
                    else:
                        print("error")
                    b = p = 0


                    if -2048 <= displacement <= 2047 and not var.isdigit():
                        p = 1



                    elif not var.isdigit():
                        b=1
                        if (var in symboltable ):
                            displacement = symboltable[var] - baseaddress["BASE"]
                        elif(var in literaltable):
                            displacement = literaltable[var] - baseaddress["BASE"]
                        else:
                            print("ERROR")
                        if(displacement>4095):
                            print("error")
                else:
                    n=1
                    i=1
                    displacement=0
                    p=0
                    b=0
                    x=0
                    e=0
                displacement &= 0xFFF  # Mask to 12 bits
                #print(p)
                opcode = opcode & 0xFC  # Clear last 2 bits of OPCODE
                nixbpe = (n << 5) | (i << 4) | (x << 3) | (b << 2) | (p << 1) | e
                object_code = (opcode << 16) | (nixbpe << 12) | displacement
                s+=f"{object_code:06X}"
                break


            elif rest[i] in format4:
                x = 0
                e = 1
                p=0
                b=0
                inputs = rest[i + 1:]

                inputs = "".join(inputs)
                operands=inputs.split(",")
                if (len(operands)>1):
                    x = 1
                    var = (operands[0])
                else:
                    x = 0
                    var = (operands[0])
                opcode = format4[rest[i]]
                n = 0
                i = 0
                if var[0] == '#':
                    n = 0
                    i = 1
                    # cut first letter
                    var = var[1:]

                elif var[0] == '@':
                    n = 1
                    i = 0
                    var = var[1:]
                else:
                    n = 1
                    i = 1
                displacement = 0
                #print(symboltable)
                if i and var.isdigit():

                    displacement = int(var)

                elif var in symboltable:
                    displacement=symboltable[var]
                elif var in literaltable:
                    displacement=literaltable[var]
                else:
                    print("ERROR")
                # Combine n and i into the first addressing bits
                ni_bits = (n << 1) | i  # Combine n and i into 2 bits (both = 1 for simple addressing)

                # Construct the first byte (6 bits opcode + 2 bits n, i)
                first_byte = (opcode & 0xFC) | ni_bits

                # Construct the second byte (x, b, p, e flags)
                second_byte = (x << 3) | (b << 2) | (p << 1) | e

                # 4. Format the address to a 20-bit value (5 hex digits)
                address_hex = format(displacement, "05X")  # Convert to uppercase 5-digit hex

                # 5. Combine everything into object code
                object_code = f"{first_byte:02X}{second_byte:01X}{address_hex}"
                s+=object_code
                break
            elif rest[i] in format4f:
                opcode = format4f[rest[i]]
                inputs=rest[i+1:]
                inputs="".join(inputs)

                operands=inputs.split(",")
                #print(operands)

                flag=0
                if(len(operands)==2):
                    var=operands[0]
                    if(operands[1]=='Z'):
                        flag=0
                    elif(operands[1]=='N'):

                        flag=1
                    elif (operands[1]=='C'):
                        flag=2
                    elif(operands[1]=='V'):
                        flag=3
                    reg=0
                else:
                    reg = registers[operands[0]]
                    var = operands[1]
                    if (operands[2] == 'Z'):
                        flag = 0
                    elif (operands[2] == 'N'):

                        flag = 1
                    elif (operands[2] == 'C'):
                        flag = 2
                    elif (operands[2] == 'V'):
                        flag = 3


                if var in symboltable:
                    displacement=symboltable[var]
                else:
                    displacement=literaltable[var]
                opcode = opcode >>2

                #print(opcode)
                #print(reg)
                #print(flag)
                #print(hex(displacement))
                # Clear last 2 bits of OPCODE
                object_code = (opcode << 26) |(reg<<22)| (flag << 20) | displacement
                s += f"{object_code:08X}"
                break
            elif(rest[i]=="WORD"):
                object_code = f"{int(rest[i+1]):06X}"
                s+=object_code
                break
            elif(rest[i]=="BYTE"):
                value=rest[i+1]
                if value.startswith("C'") and value.endswith("'"):
                    # Character constant: Convert each character to its ASCII hex value
                    chars = value[2:-1]  # Remove C' and ending '
                    object_code = ''.join(f"{ord(char):02X}" for char in chars)
                    s+=object_code
                elif value.startswith("X'") and value.endswith("'"):
                    # Hexadecimal constant: Directly use the provided hex value
                    hex_value = value[2:-1]  # Remove X' and ending '
                    s+=hex_value
                break
            elif (rest[i]=="*"):
                value=rest[i+1]
                if value.startswith("=C'") and value.endswith("'"):
                    # Character constant: Convert each character to its ASCII hex value
                    chars = value[3:-1]  # Remove =C' and ending '
                    object_code = ''.join(f"{ord(char):02X}" for char in chars)
                    s+=object_code
                elif value.startswith("=X'") and value.endswith("'"):
                    # Hexadecimal constant: Directly use the provided hex value
                    hex_value = value[3:-1]  # Remove =X' and ending '
                    s+=hex_value
                break
            elif(rest[i]=="USE" or rest[i]=="RESW" or rest[i]=="RESB"):
                #print("da5alt")
                s=" "
                break

        #print(s)
        with open("output_pass2.txt", "a") as file4:
            file4.write(s + "\n")


pass2()
