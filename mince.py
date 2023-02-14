from os import system
from sys import argv
from time import time

VERSION = 1.0


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
            b = (b <= MathExpression(act)+1)
        elif TakeString("<"):
            b = (b < MathExpression(act)+1)
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
            elif TakeString("\\t"):
                s += '\t'
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

    if not TakeNext('=') or ident == "":
        Error("unknown statement")

    e = Expression(act)

    if act[0] or ident not in variable:
        # assert initialization even if block is inactive
        variable[ident] = e

def DoReturn(act):
    ident = TakeNextAlNum()
    e = Expression(act)
    if act[0] or ident not in variable:
        variable[ident] = e

def DoRun(act):
    ident = TakeNextAlNum()

    e = Expression(act)

    system(e[1])

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
            print(e[1], end="")
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
    e = Expression(act) 
    f =  Expression(act)

    new = list(variable[e[1]])
    new[1] += int(f[1])
    variable[e[1]] = tuple(new)

def Decrement(act):
    e = Expression(act) 
    f =  Expression(act)

    new = list(variable[e[1]])
    new[1] -= int(f[1])
    variable[e[1]] = tuple(new)


def DoError(act):
    ident, e, line = TakeNextAlNum(), Expression(act), str(source[:pc].count("\n"))

    try:
        print(f"mince: " + argv[1] + ":" + str(line) + ":" + " " + e[1])
        exit(1)
    except TypeError as e:
        raise e

    # if act[0] or ident not in variable:
    #     variable[ident] = e

def GetMinimum(act):
    e = Expression(act)
    f = Expression(act)
    g = Expression(act)
    h = Expression(act)
    i = Expression(act)
    l = [e[1], f[1], g[1], h[1], i[1]]

    res = min(l)

    variable["min"] = ('i', res)


def GetMaximum(act):
    e = Expression(act)
    f = Expression(act)
    g = Expression(act)
    h = Expression(act)
    i = Expression(act)

    l = [e[1], f[1], g[1], h[1], i[1]]

    res = max(l)

    variable["max"] = ('i', res)


def Statement(act):

    if TakeString("inc"):
        Increment(act)
    elif TakeString("dec"):
        Decrement(act)
    elif TakeString("min"):
        GetMinimum(act)
    elif TakeString("max"):
        GetMaximum(act)
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
    elif TakeString("def"):
        DoFunDef()
    else:
        DoAssign(act)


def Block(act):
    if TakeNext("{"):
        while not TakeNext("}"):
            Block(act)
    else:
        Statement(act)


def Program():
    act = [True]
    while Next() != '\0':
        Block(act)

def Error(text):
    s, e = source[:pc].rfind("\n") + 1, source.find("\n", pc)

    print("mince: " + argv[2] + ":" +
          str(source[:pc].count("\n")+1) + ": " +
          text + " near " + "\n\t'" + source[s:pc] +
          "_" + source[pc:e] + "'")

    exit(1)

def usage():
    print(f"Help: {argv[0]} [options] <file>")
    print(" -h  --help | show this help menu and exit.")
    print("commands:")
    print(" run <file> | run/evaluate the file.")
    print(" compile <file> | compile the file to c.")

def show_version():
    print(VERSION)
pc = 0
variable = {}

if len(argv) < 2: 
    print("Usage: mince [options] <file>")
    print("No arguments provided!")
    exit(1)

try:
    if argv[1] == 'run' or argv[1] == '-r':
        f = open(argv[2], 'r')
        source = f.read() + '\0'

        f.close()

        Program()
    elif argv[1]== 'compile' or argv[1] == '-c':
        NotImplemented("COMPILING TO C")
    elif argv[1] == 'init' or argv[1] == '-i':
        if argv[2] == '.':
            system("touch Main.mc")
            with open("Main.mc", "w") as f:
                f.write("def main {\n")
                f.write("   print \"Hello world\"\n")
                f.write("}\n")
                f.write("\n")
                f.write("inv main\n")
            system("git init -q")
        else:
            system(f"mkdir {argv[2]} && cd {argv[2]} && touch Main.mc && git init -q")
            with open(f"{argv[2]}/Main.mc", "w") as f:
                f.write("def main {\n")
                f.write("   print \"Hello world\"\n")
                f.write("}\n")
                f.write("\n")
                f.write("inv main\n")

    elif argv[1] == '-h' or argv[1] == 'help':
        usage()
    elif argv[1] == '-V' or argv[1] == "--version":
        show_version()
    else:
        print("Unrecognized option/command")
        print("Try -h/--help to get help")
        exit(1)

except FileNotFoundError:
    print("ERROR: Can't find source file \'" + argv[1] + "\'.")
    exit(1)
