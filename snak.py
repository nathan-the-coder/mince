#!/usr/bin/env python3

import argparse
import os
import sys
import platform

if platform.platform().startswith("Linux"):
    import log
elif platform.platform().startswith("Windows"):
    from scripts import log

# returns the current character while skipping over comments
def Look():
    # comments are entered by # and exited by \n or \0
    global pc
    global source

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
    elif TakeString("val("):
        s = String(act)
        if act[0] and s.isdigit():
            m = int(s)
        if not TakeNext(')'):
            Error("missing ')'")
    else:
        ident = TakeNextAlNum()
        if ident not in variable or variable[ident][0] != 'i':
            if ident == "false":
                return False
            elif ident == "true":
                return True
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
    #str(...)
    elif TakeString("str("):
        s = str(MathExpression(act))
        if not TakeNext(')'):
            Error("missing ')'")
    elif TakeString("input()"):
        if act[0]:
            s = input()
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


def DoWhile(act):
    global pc
    local = [act[0]]
    # save PC of the while statement
    pc_while = pc
    while BooleanExpression(local):
        Block(local)
        pc = pc_while
    # scan over inactive block and leave while
    Block([False])


def DoIfElse(act):
    b = BooleanExpression(act)
    if act[0] and b:
        # process if block?
        Block(act)
    else:
        Block([False])
    Next()
    # process else block?
    if TakeString("else"):
        if act[0] and not b:
            Block(act)
        else:
            Block([False])


def DoGoSub(act):
    global pc, stack
    ident = TakeNextAlNum()
    if ident not in variable or variable[ident][0] != 'p':
        Error("unknown method")
    ret = pc
    pc = variable[ident][1]
    Block(act)
    # execute block as a subroutine
    pc = ret
    stack.append(ident)


def DoSubDef():
    global pc
    global methods
    ident = TakeNextAlNum()
    if ident == "":
        Error("missing method identifier")
    variable[ident] = ('p', pc)
    methods += 1
    Block([False])


def DoAssign(act):
    global vars
    ident = TakeNextAlNum()
    if not TakeNext('=') or ident == "":
        if ident == "include":
            pass
        elif ident == "game":
            pass
        else:
            Error("unknown statement")

    if ident == "false":
        return 1
    elif ident == "true":
        return 0

    
    e = Expression(act)
    if act[0] or ident not in variable:
        # assert initialization even if block is inactive
        variable[ident] = e
        vars.append(ident)


def DoReturn(act):
    ident = TakeNextAlNum()
    e = Expression(act)
    if act[0] or ident not in variable:
        variable[ident] = e
    return ident or e

def print_stack():
    global vars
    global methods
    global stack
    global stdout

    ident = TakeNextAlNum()
    if ident == "":
        Error("missing stack identifier")
    
    if ident == "vars":
        print(vars)
    elif ident == "methods":
        print("methods:", methods)
    elif ident == "stack":
        print(stack)
    elif ident == "stdout":
        print(stdout)


def DoBreak(act):
    if act[0]:
        # switch off execution within enclosing loop (while, ...)
        act[0] = False


def DoPrint(act):
    global stdout
    # process comma-separated arguments
    while True:
        e = Expression(act)
        if act[0]:
            print(e[1], end="\n")
            stdout.append(e[1])
        if not TakeNext(','):
            return


def DoExit(act):
    e = Expression(act)
    exit(e[1])

def Statement(act):
    append = "<<"
    out = ">>"

    if TakeString("stdout " + append):
        DoPrint(act)
    elif TakeString("exit"):
        DoExit(act)
    elif TakeString("ret"):
        DoReturn(act)
    elif TakeString("if"):
        DoIfElse(act)
    elif TakeString("while"):
        DoWhile(act)
    elif TakeString("break"):
        DoBreak(act)
    elif TakeString("stack " + out):
        DoGoSub(act)
    elif TakeString("method " + append):
        DoSubDef()
    elif TakeString("dump " + out):
        print_stack()
    else:
        DoAssign(act)


def Block(act):
    if TakeNext("["):
        while not TakeNext("]"):
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
    print("\nERROR " + text + " in line " +
          str(source[:pc].count("\n") + 1) + ": '" + source[s:pc] + "_" + source[pc:e] + "'\n")
    sys.exit(1)



# --------------------------------------------------------------------------------------------------

stack = []
methods = 0
stdout = []
vars = []

pc = 0
# program couter, identifier -> (type, value) lookup table
variable = {}



if os.path.isfile(sys.argv[1]):
    try:
        f = open(sys.argv[1], 'r')

    except FileNotFoundError:
        print("ERROR: Can't find source file \'" + sys.argv[1] + "\'.")
        sys.exit(1)

    # Dectect file extension
    if sys.argv[1].endswith('.sn'):
        pass
    else:
        log.Log(3, 'Source file is not support!')
    
    # append a null termination
    source = f.read() + '\0'


    f.close()

    Program()

else:

    if sys.argv[1].startswith('-'):

        ap = argparse.ArgumentParser()
        ap.add_argument("-e", "--edit", help="edit source file using the Snak editor")
        arg = ap.parse_args()

        if os.path.isfile(arg.edit) and str(arg.edit).endswith(".sn"):
            if os.system("sedit"):
                os.system(f"sedit {arg.edit}")
            else:
                os.system(f"./sedit/sedit {arg.edit}")
        else:
            raise Exception("Cannot edit non source file.")
    else:
        f = open(sys.argv[2], 'r')

