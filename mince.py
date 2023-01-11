#!/usr/bin/env python3

import os
import sys

VERSION = 0.1

# returns the current character while skipping over comments
def Look():
    # comments are entered by # and exited by \n or \0
    global pc

    if source[pc] == '#':
        while source[pc] != '\n' and source[pc] != '\0':
            # scan over comments here
            pc += 1
    return source[pc]


# takes away and returns the current character
def Take():
    global pc
    c = Look()
    pc += 1
    return c


# returns whether a certain string could be taken starting at pc
def TakeString(word):
    global pc
    copypc = pc
    for c in word:
        if Take() != c:
            pc = copypc
            return False
    return True


# returns the next non-whitespace character
def Next():
    while Look() == ' ' or Look() == '\t' or Look() == '\n' or Look() == '\r':
        Take()
    return Look()


# eats white-spaces, returns whether a certain character could be eaten
def TakeNext(c):
    if Next() == c:
        Take()
        return True
    else:
        return False


# recognizers
def IsDigit(c): return (c >= '0' and c <= '9')
def IsAlpha(c): return ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'))
def IsAlNum(c): return (IsDigit(c) or IsAlpha(c))
def IsAddOp(c): return (c == '+' or c == '-')
def IsMulOp(c): return (c == '*' or c == '/')


def TakeNextAlNum():
    alnum = ""
    if IsAlpha(Next()):
        while IsAlNum(Look()):
            alnum += Take()
    return alnum

# --------------------------------------------------------------------------------------------------


def BooleanFactor(act):
    inv = TakeNext('!')
    e = Expression(act)
    b = e[1]
    Next()
    # a single mathexpression may also serve as a boolean factor
    if (e[0] == 'i'):
        if TakeString("=="):
            b = (b == MathExpression(act))
        elif TakeString("!="):
            b = (b != MathExpression(act))
        elif TakeString("<="):
            b = (b <= MathExpression(act))
        elif TakeString("<"):
            b = (b < MathExpression(act))
        elif TakeString(">="):
            b = (b >= MathExpression(act))
        elif TakeString(">"):
            b = (b > MathExpression(act))
    else:
        if TakeString("=="):
            b = (b == StringExpression(act))
        elif TakeString("!="):
            b = (b != StringExpression(act))
        else:
            b = (b != "")
    # always returns False if inactive
    return act[0] and (b != inv)


def BooleanTerm(act):
    b = BooleanFactor(act)
    while TakeString('&&'):
        # logical and corresponds to multiplication
        b = b & BooleanFactor(act)
    return b


def BooleanExpression(act):
    b = BooleanTerm(act)
    while TakeString('||'):
        # logical or corresponds to addition
        b = b | BooleanTerm(act)
    return b


def MathFactor(act):
    m = 0
    if TakeNext('('):
        m = MathExpression(act)
        if not TakeNext(')'):
            Error("missing ')'")
    elif IsDigit(Next()):
        while IsDigit(Look()):
            m = 10 * m + ord(Take()) - ord('0')
    else:
        ident = TakeNextAlNum()
        if ident not in variable or variable[ident][0] != 'i':
            if ident == "false":
                return False
            elif ident == "true":
                return True
            elif ident == "inv":
                DoCallFun(act)
            elif ident == "defun":
                DoFunDef()
            elif ident == "print":
                DoPrint(act)
            elif ident == "then" or ident == "end":
                pass
            else:
                Error("unknown variable")
        elif act[0]:
            m = variable[ident][1]
    return m


def MathTerm(act):
    m = MathFactor(act)
    while IsMulOp(Next()):
        c = Take()
        m2 = MathFactor(act)
        if c == '*':
            # multiplication
            m = m * m2
        else:
            # division
            m = m / m2
    return m


def MathExpression(act):
    # check for an optional leading sign
    c = Next()
    if IsAddOp(c):
        c = Take()
    m = MathTerm(act)
    if c == '-':
        m = -m
    while IsAddOp(Next()):
        c = Take()
        m2 = MathTerm(act)
        if c == '+':
            # addition
            m = m + m2
        else:
            # subtraction
            m = m - m2
    return m


def String(act):
    s = ""
    # is it a literal string?
    if TakeNext('\"'):
        while not TakeString("\""):
            if Look() == '\0':
                Error("unexpected EOF")
            if TakeString("\\n"):
                s += '\n'
            else:
                s += Take()
    else:
        ident = TakeNextAlNum()

        if ident in variable and variable[ident][0] == 's':
            s = variable[ident][1]
        else:
            Error("not a string")

    return s


def StringExpression(act):
    s = String(act)
    while TakeNext('+'):
        # string addition = concatenation
        s += String(act)
    return s


def Expression(act):
    global pc

    copypc = pc

    ident = TakeNextAlNum()

    # scan for identifier or "str"
    pc = copypc

    if(Next() == '\"' or ident == "str"
            or ident == "input"
            or (ident in variable and variable[ident][0] == 's')):
        return ('s', StringExpression(act))
    else:
        return ('i', MathExpression(act))


def WBlock(act):
    if TakeNext("do"):
        while not TakeNext("end"):
            WBlock(act)
    else:
        Statement(act)

def DoWhile(act):
    global pc

    local = [act[0]]

    # save PC of the while statement
    pc_while = pc

    while BooleanExpression(local):
        WBlock(local)
        pc = pc_while

    # scan over inactive block and leave while
    WBlock([False])


def IFBlock(act):
    if TakeNext("then"):
        while not TakeNext(""):
            IFBlock(act)
    else:
        Statement(act)

def ELSEBlock(act):
    if TakeNext(""):
        while not TakeNext("end"):
            ELSEBlock(act)
    else:
        Statement(act)

def DoIfElse(act):
    b = BooleanExpression(act)

    if act[0] and b:
        # process if block?
        IFBlock(act)
    else:
        IFBlock([False])

    Next()

    # process else block?
    if TakeString("else"):
        if act[0] and not b:
            ELSEBlock(act)
        else:
            ELSEBlock([False])


def DoCallFun(act):
    global pc
    ident = TakeNextAlNum()

    if ident not in variable or variable[ident][0] != 'p':
        Error("unknown function")

    ret = pc
    pc = variable[ident][1]

    Block(act)

    # execute block as a subroutine
    pc = ret


def DoFunDef():
    global pc

    ident = TakeNextAlNum()

    if ident == "":
        Error("missing function identifier")

    variable[ident] = ('p', pc)
    Block([False])


def DoAssign(act):
    ident = TakeNextAlNum()

    if ident == "then" or ident == "end":
        pass
    else:
        if not TakeNext('=') or ident == "":
            Error("unknown statement")

    e = Expression(act)

    if e[1] == "false":
        return 1
    elif e[1] == "true":
        return 0

    if act[0] or ident not in variable:
        # assert initialization even if block is inactive
        variable[ident] = e


def DoReturn(act):
    ident = TakeNextAlNum()
    e = Expression(act)
    if act[0] or ident not in variable:
        variable[ident] = e
    return e[1]


def DoRun(act):
    ident = TakeNextAlNum()

    e = Expression(act)

    os.system(e[1])

    if act[0] or ident not in variable:
        variable[ident] = e


def DoBreak(act):
    if act[0]:
        # switch off execution within enclosing loop (while, ...)
        act[0] = False


def DoPrint(act):
    # process comma-separated arguments
    while True:
        e = Expression(act)
        if act[0]:
            print(e[1])
        if not TakeNext(','):
            return


def DoExit(act):
    e = Expression(act)
    exit(e[1])



def DoRead(act):
    ident = TakeNextAlNum()

    f1 = Expression(act)
    e = Expression(act)

    with open(f1[1], "r") as f:
        if e is not None:
            print(f.read(e[1]))
        else:
            print(f.read())

    if act[0] or ident not in variable:
        variable[ident] = e


def DoWrite(act):
    global pc
    ident = TakeNextAlNum()

    e = Expression(act)
    fi = Expression(act)

    with open(e[1], "w+") as f:
        f.write(fi[1])


    if act[0] or ident not in variable:
        variable[ident] = e
  
def Increment(act):
    global pc
    ident = TakeNextAlNum()

    e = Expression(act)

    print(e[1])


    if act[0] or ident not in variable:
        variable[ident] = e

def DoError(act):
    ident = TakeNextAlNum()

    e = Expression(act)
    line = str(source[:pc].count("\n"))

    try:
        print(f"mince: " + sys.argv[1] + ":" + str(line) + ":" + " " + e[1])
        exit(1)
    except TypeError as e:
        raise e

    if act[0] or ident not in variable:
        variable[ident] = e

def Statement(act):

    if TakeString("inc"):
        NotImplemented("Error: Not Implemented Yet!")
    elif TakeString("dec"):
        NotImplemented("Error: Not Implemented Yet!")
    elif TakeString("print"):
        DoPrint(act)
    elif TakeString("exit"):
        DoExit(act)
    elif TakeString("return"):
        DoReturn(act)
    elif TakeString("read"):
        DoRead(act)
    elif TakeString("write"):
        DoWrite(act)
    elif TakeString("exec"):
        DoRun(act)
    elif TakeString("panic"):
        DoError(act)
    elif TakeString("if"):
        DoIfElse(act)
    elif TakeString("while"):
        DoWhile(act)
    elif TakeString("break"):
        DoBreak(act)
    elif TakeString("inv"):
        DoCallFun(act)
    elif TakeString("defun"):
        DoFunDef()
    else:
        DoAssign(act)


def Block(act):
    if TakeNext(""):
        while not TakeNext("end"):
            Block(act)
    else:
        Statement(act)


def Program():
    act = [True]
    while Next() != '\0':
        Block(act)

def Error(text):
    s = source[:pc].rfind("\n") + 1
    e = source.find("\n", pc)

    print("mince: " + sys.argv[1] + ":" +
          str(source[:pc].count("\n")+1) + ": " +
          text + " near " + "\n\t'" + source[s:pc] +
          "_" + source[pc:e] + "'")

    sys.exit(1)


def version():
    print(f"""
mince: version {VERSION} 
by: Nathaniel Ramos <nathanielramos726@gmail.com>

INFO:
* The development started on July 7 2022
""")

def help():
    print("HELP: mince <options> <file>")
    print("options: ")
    print("    -v | --version | show some information and mince version")
    print("    -h | --help    | show this help menu")
# --------------------------------------------------------------------------------------------------


pc = 0
# program couter, identifier -> (type, value) lookup table
variable = {}

if len(sys.argv) < 2: 
    print("Usage: mince <file>")
    print("No arguments provided!")
    exit(1)

if sys.argv[1] == "-v" or sys.argv[1] == "--version":
    version()
elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    help()
else:
    try:
        f = open(sys.argv[1], 'r')

        # append a null termination
        source = f.read() + '\0'

        f.close()

        Program()

    except FileNotFoundError:
        print("ERROR: Can't find source file \'" + sys.argv[1] + "\'.")
        sys.exit(1)