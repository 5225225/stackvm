import sys
import shlex
from enum import Enum

stack = []

class opcode(Enum):
    PUSH = 1
    ADD = 2
    SUB = 3
    MULT = 4
    DIV = 5
    MOD = 6
    JEQ = 7
    GOTO = 8
    PRINT = 9
    INPUT = 10
    CAST = 11
    DUPE = 12
    HLT = 13;


class dtype(Enum):
    INT = 1
    STR = 2

class command:
    def __init__(self, op, operands):
        self.op = opcode[op]
        self.operands = operands

    def __repr__(self):
        return "command({}, {})".format(self.op, self.operands)

def convert_to(obj, dt):
    if dt == dtype.INT:
        return int(obj)
    if dt == dtype.STR:
        return str(obj)

def execute(cmd):
    global increment
    global ptr

    # Used for jumping instructions

    if cmd.op == opcode.PUSH:
        offset = 0
        datatype = dtype.INT
        if cmd.operands[0] == "@":
            datatype = dtype[cmd.operands[1].upper()]
            offset = 2


        for arg in cmd.operands[offset:]:
            stack.append(convert_to(arg, datatype))

    if cmd.op == opcode.ADD:
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(arg1 + arg2)

    if cmd.op == opcode.SUB:
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(arg1 - arg2)

    if cmd.op == opcode.MULT:
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(arg1 * arg2)

    if cmd.op == opcode.DIV:
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(arg1 / arg2)

    if cmd.op == opcode.MOD:
        arg2 = stack.pop()
        arg1 = stack.pop()
        stack.append(arg1 % arg2)

    if cmd.op == opcode.JEQ:

        linenum = stack.pop()
        arg1 = stack.pop()
        arg2 = stack.pop()

        if arg1 == arg2:
            increment = False
            ptr = linetoindex[linenum]

    if cmd.op == opcode.GOTO:

        linenum = stack.pop()
        increment = False
        ptr = linetoindex[linenum]

    if cmd.op == opcode.PRINT:
        toprint = stack.pop()
        print(toprint)

    if cmd.op == opcode.INPUT:
        stack.append(input())

    if cmd.op == opcode.CAST:
        datatype = dtype[stack.pop()]
        obj = stack.pop()
        stack.append(convert_to(obj, datatype))

    if cmd.op == opcode.DUPE:
        obj = stack.pop()
        stack.append(obj)
        stack.append(obj)

    if cmd.op == opcode.HLT:
        sys.exit(0)
            
if len(sys.argv) > 1:
    lex = shlex.shlex(open(sys.argv[1]) ,posix=True)
else:
    lex = shlex.shlex(posix=True)

cmds = []
linetoindex = {}

while True:
    cmd = lex.get_token()
    linenum = lex.lineno
    if cmd is None:
        break

    args = [lex.get_token()]
    if args[0] is not None:
        while args[-1] not in (None, ";"):
            args.append(lex.get_token())

    args.pop() # Gets rid of the terminator.

    if cmd == ":":
        linetoindex[args[0]] = len(cmds)
    else:
        linetoindex[linenum] = len(cmds)
        cmds.append(command(cmd, args))

ptr = 0

while True:
    if ptr >= len(cmds):
        break

    increment = True
    execute(cmds[ptr])

    if increment:
        ptr += 1


print("\n=== Dumping stack contents ===")
for index, item in enumerate(stack):
    print("{}\t{} {}".format(index, str(type(item)), item))
