from formatmaps import format1, format2, format3, format4, format4f


def get_literal_length(literal):
    if literal.startswith("=X'"):  # Hexadecimal literal
        return (len(literal) - 4) // 2  # Exclude =X' and '
    elif literal.startswith("=C'"):  # Character literal
        return len(literal) - 4  # Exclude =C' and '
    else:  # Numeric literal
        return 3  # Default word size in SIC/XE


def get_byte_length(literal):
    if literal.startswith("X'"):  # Hexadecimal literal
        return 1
    elif literal.startswith("C'"):  # Character literal
        return len(literal) - 4  # Exclude =C' and '
    else:  # Numeric literal
        return 3  # Default word size in SIC/XE


def pass1():
    with open("INTERMEDIATE.txt", "w") as file:
        file.write("")
    with open("symboltable.txt", "w") as file:
        file.write("")
    with open("code.txt", "r") as file:
        # Read all lines from the file
        lines = file.readlines()
    with open("OUTPUT_PASS1.txt", "w") as file:
        file.write("")

    mapblcks = {
        "DEFAULT": 0,
        "CDATA": 0,
        "CBLKS": 0,
        "DEFAULTB": 0

    }
    currentblock = "DEFAULT"
    literals = []
    literalsglobal = []
    base = ""
    for line in lines:

        # Split the line into words
        words = line.split()
        # Access each word
        incvalue = 0
        s = ""
        s3 = ""
        if len(words) != 0:
            s += currentblock

            s += " "

            s += str(hex(mapblcks[currentblock]))
            s3 += currentblock

            s3 += " "

            s3 += str(hex(mapblcks[currentblock]))
        f = 0
        f3 = 0
        for i in range(0, len(words)):
            #print(words[i])
            if words[i] == "START":
                defaultcounter = int(words[i + 1], 16)
                mapblcks["DEFAULT"] = 0
                s += " "
                s += words[i]
                f3 = 1
            elif words[i] == "BASE":
                base = words[i + 1]
                f = 1
            elif words[i] in format1:
                incvalue = 1
                s += " "
                s += words[i]
            elif words[i] in format2:
                incvalue = 2
                s += " "
                s += words[i]
            elif words[i] in format3:
                incvalue = 3
                s += " "
                s += words[i]
            elif words[i] in format4:
                incvalue = 4
                s += " "
                s += words[i]
            elif words[i] in format4f:
                incvalue = 4
                s += " "
                s += words[i]
            elif words[i] == "USE":
                # print(len(words))
                # print(words)
                if (len(words) == 1):
                    s = ""

                    s = s+ "DEFAULT"
                    s = s + " "
                    s = s+ str(hex(mapblcks["DEFAULT"]))
                    s = s+" "
                    currentblock = "DEFAULT"
                    s += " "
                    s += words[i]

                elif(words[i+1]==';' or words[i+1][0]==';'):
                    s = s+ "DEFAULT"
                    s = s + " "
                    s = s+ str(hex(mapblcks["DEFAULT"]))
                    s = s+" "
                    currentblock = "DEFAULT"
                    s += " "
                    s += words[i]

                else:
                    s=""
                    s = s + words[i + 1]
                    s = s + " "
                    s = s + str(hex(mapblcks[words[i + 1]]))
                    s = s + " "
                    currentblock = words[i + 1]
                    if (words[i + 1] not in mapblcks):
                        # print ("error et2ay allh ya programmer")
                        print("errrrrror")
                    s += " "
                    s += words[i]
                f3 = 1

            elif words[i] == "RESW":
                incvalue = int(words[i + 1]) * 3
                s += " "
                s += words[i]
            elif words[i] == "RESB":
                incvalue = int(words[i + 1])
                s += " "
                s += words[i]
            elif words[i] == "WORD":
                incvalue = 3
                s += " "
                s += words[i]
            elif words[i] == "BYTE":
                incvalue = get_byte_length(words[i + 1])
                s += " "
                s += words[i]
            elif words[i][0] == '=':
                #print(words[i])
                #print(len(words[i]))
                if (words[i] not in literalsglobal):
                    literals.append(words[i])
                    literalsglobal.append(words[i])

                s += " "
                s += words[i]
            elif words[i] == "LTORG":
                for i in range(0, len(literals)):
                    s1 = ""

                    s1 += currentblock

                    s1 += " "

                    s1 += str(hex(mapblcks[currentblock]))
                    s1 += " "
                    s1 += '*'
                    s1 += " "
                    s1 += literals[i]
                    #print(literals[i])
                    #print(get_literal_length(literals[i]))
                    mapblcks[currentblock] += get_literal_length(literals[i])
                    if (len(s1) > 0):
                        with open("INTERMEDIATE.txt", "a") as file:
                            file.write(s1 + "\n")
                literals.clear()
                f = 1
            elif words[i] == ";" or words[i][0] == ';':
                break
            elif words[i] == "END":
                for i in range(0, len(literals)):
                    s1 = ""

                    s1 += currentblock

                    s1 += " "

                    s1 += str(hex(mapblcks[currentblock]))
                    s1 += " "
                    s1 += '*'
                    s1 += " "
                    s1 += literals[i]
                    # print(literals[i])
                    mapblcks[currentblock] += get_literal_length(literals[i])
                    if (len(s1) > 0):
                        with open("INTERMEDIATE.txt", "a") as file:
                            file.write(s1 + "\n")
                s = ""
                s += "CBLKS"

                s += " "

                s += str(hex(mapblcks["CBLKS"]))
                s += " "
                s += "END"
                s += " "
                f3 = 1
            else:
                s += " "
                s += words[i]

        if (len(s) > 0 and f != 1):
            with open("INTERMEDIATE.txt", "a") as file:
                file.write(s + "\n")


        else:
            f = 0
        if (len(s3) > 0 and f != 1 and f3 != 1):
            with open("OUTPUT_PASS1.txt", "a") as file:
                file.write(s3 + "\n")
                f3 = 0
        mapblcks[currentblock] += incvalue

    with open("INTERMEDIATE.txt", "r") as file:
        # Read all lines from the file
        lines = file.readlines()
    startblocks = {
        "DEFAULT": defaultcounter,
        "DEFAULTB": defaultcounter + mapblcks["DEFAULT"],
        "CDATA": (defaultcounter + mapblcks["DEFAULTB"] + mapblcks["DEFAULT"]),

        "CBLKS": (defaultcounter + mapblcks["DEFAULTB"] + mapblcks["CDATA"] + mapblcks["DEFAULT"]),

    }
    symboltable = {}
    literaltable = {}
    m = 0
    for line in lines:
        # Split the line into words
        if (m == 0):
            m = 1
            continue

        words = line.split()

        if (words[2] not in format1 and words[2] not in format2 and
                words[2] not in format3 and words[2] not in format4 and words[2] != "USE"
                and words[2] != "START" and words[2] != "END" and words[2] not in format4f):
            if (words[2] == "*"):
                literaltable[words[3]] = startblocks[words[0]] + int(words[1], 16)
            elif (words[2] not in symboltable):
                symboltable[words[2]] = startblocks[words[0]] + int(words[1], 16)

            else:
                print("error")
                break

    with open("symboltable.txt", "w") as file:
        for key, value in symboltable.items():
            file.write(f"{key}: {hex(value)}\n")
    with open("literaltable.txt", "w") as file:
        for key, value in literaltable.items():
            file.write(f"{key}: {hex(value)}\n")
    with open("blockstarting.txt", "w") as file:
        for key, value in startblocks.items():
            file.write(f"{key}: {hex(value)}\n")
    s = "BASE"
    with open("base.txt", "w") as file:
        file.write(f"{s}: {hex(symboltable[base])}\n")


pass1()
