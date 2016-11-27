import sys
import base64

codefile = open(sys.argv[1]).read()

code = []
for item in codefile.split("\n"):
    item = item.strip()
    if item:
        toktype, b64val = item.split(" ")
        value = base64.b64decode(b64val).decode("UTF-8")
        if toktype == "NUMBER":
            value = int(value)
        code.append((toktype, value))

for index, item in enumerate(code):
    print("{:04d} | {}\t{}".format(index, item[0], item[1]))

datastack = []
returnstack = []
mem = [0]*(1<<16)

pc = 0
incpc = True
print("\n---\n")
while pc < len(code):
    toktype, value  = code[pc]
    print("{:04d} | {}\t{}".format(pc, toktype, value))
    for item in datastack:
        print("  " + str(item))
    print()


    if toktype in ("NUMBER", "STRING"):
        datastack.append(value)

    elif toktype == "OPER":
        
        if value == "ADD":
            y = datastack.pop()
            x = datastack.pop()
            datastack.append(x + y)

        elif value == "SUB":
            y = datastack.pop()
            x = datastack.pop()
            datastack.append(x - y)

        elif value == "MULT":
            y = datastack.pop()
            x = datastack.pop()
            datastack.append(x * y)

        elif value == "DIV":
            y = datastack.pop()
            x = datastack.pop()
            datastack.append(x // y)

        elif value == "MOD":
            y = datastack.pop()
            x = datastack.pop()
            datastack.append(x % y)

        elif value == "DUP":
            x = datastack.pop()
            datastack.append(x)
            datastack.append(x)
        
        elif value == "DROP":
            _ = datastack.pop()

        elif value == "SWAP":
            x = datastack.pop()
            y = datastack.pop()

            datastack.append(x)
            datastack.append(y)

        elif value == "RROT":
            n = datastack.pop()

            x = datastack.pop(-n)

            datastack.append(x)

        elif value == "LROT":
            n = datastack.pop()

            x = datastack.pop()

            datastack.insert(-n + 1, x)

        elif value == "JUMP":
            pc = datastack.pop()
            incpc = False

        elif value == "JEQ":
            newpc = datastack.pop()
            val2 = datastack.pop()
            val1 = datastack.pop()
            print(val1 == val2)
            if val1 == val2:
                pc = newpc
                incpc = False

        elif value == "JENQ":
            newpc = datastack.pop()
            val2 = datastack.pop()
            val1 = datastack.pop()
            if val1 == val2:
                pc = newpc
                incpc = False

        elif value == "JGT":
            newpc = datastack.pop()
            val2 = datastack.pop()
            val1 = datastack.pop()
            if val1 > val2:
                pc = newpc
                incpc = False

        elif value == "JLT":
            newpc = datastack.pop()
            val2 = datastack.pop()
            val1 = datastack.pop()
            if val1 < val2:
                pc = newpc
                incpc = False

        elif value == "CALL":
            newpc = datastack.pop()
            returnstack.append(pc + 1)
            pc = newpc
            incpc = False

        elif value == "RETURN":
            newpc = returnstack.pop()
            pc = newpc
            incpc = False


        elif value == "PUSHPC":
            datastack.append(pc)

        elif value == "PRINT":
            val = datastack.pop()

            print(val)

        elif value == "GETMEM":
            addr = datastack.pop()

            datastack.append(mem[addr])

        elif value == "SETMEM":
            val = datastack.pop()
            addr = datastack.pop()

            mem[addr] = val % 256

        elif value == "GETCHAR":
            ch = sys.stdin.buffer.read(1)
            if ch:
                datastack.append(ord(ch))
            else:
                datastack.append(-1)

        elif value == "PUTCHAR":
            ch = datastack.pop()
            if 0 <= ch <= 256:
                sys.stdout.buffer.write(bytes([ch]))

        elif value == "DEBUG":
            print("--- Debug ---")
            print(" -- Stack --")
            for item in datastack:
                print("  " + str(item))
            print(" -- End Stack --")

            with open("/tmp/stackvm.bin", "wb") as f:
                for x in mem:
                    f.write(x.to_bytes(1, "big"))
            print(" -- Wrote memory contentx to /tmp/stackkvm.bin --")
            print("--- End Debug ---")
        

    if incpc:
        pc += 1
    incpc = True
