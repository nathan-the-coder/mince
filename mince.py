#!/usr/bin/env python3
# type: ignore

import os
import sys

modules = ["tk"]
debug = False


# returns the current character while skipping over comments
def Look():
    # comments are entered by # and exited by \n or \0
    global pc

    if source[pc] == '/' and source[pc+1] == '/':
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
    while TakeString('and'):
        # logical and corresponds to multiplication
        b = b & BooleanFactor(act)
    return b


def BooleanExpression(act):
    b = BooleanTerm(act)
    while TakeString('or'):
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

        function_params = {}

        for v in variables:
            func = variables[v]
            if func[0] == 'p':
                for param in func[-1]:
                    function_params[param] = func[-1][param]

        if ident not in variables or variables[ident][0] != 'i':
            if ident not in function_params:
                Error(f"unknown variables: '{ident}'")
        elif act[0]:
            m = variables[ident][1]
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
    if TakeNext('"'):
        while True:
            # escaped newline
            if TakeString("\\n"):
                s += '\n'
            # escape qoute
            elif TakeString("\\\""):
                s += "\""
            # Interpolation start
            elif TakeString("${"):
                # parse any Expression
                expr = Expression(act)
                if not TakeNext("}"):
                    Error("missing '}' in string interpolation")
                # splice its text form
                s += str(expr[1])
            # end of string
            elif Look() == '"':
                Take()
                break
            elif Look() == '\0':
                Error("unexpected EOF in string literal")
            # plain character
            else:
                s += Take()

    else:
        ident = TakeNextAlNum()
        if ident in variables and variables[ident][0] == 's':
            s = variables[ident][1]
        else:
            if ident in variables and variables[ident][0] == 'i':
                s = s + str(variables[ident][1])
            # Error("not a string")

    return s


def StringExpression(act):
    s = String(act)

    while TakeNext('+'):
        # string addition = concatenation
        s += String(act)
    return s


def DataExpression(act):
    global pc
    data = {}  # Store the parsed fields
    
    # Parse the type (User, for example)
    type_name = TakeNextAlNum()  # "User"
    if not type_name:
        Error("Expected type name before '{'")
    
    # Expect '{' after the type name to start parsing fields
    if not TakeNext("{"):
        Error("Expected '{' to start object definition")
    Next()
    
    while True:
        # Parse the field names and values
        field_name = TakeNextAlNum()
        if not field_name:
            break  # No more fields
        
        # Expect '=' to start assignment of the field value
        if not TakeNext(":"):
              Error("Expected ':' after field name")
        Next()

        # Parse the field value (could be string, number, etc.)
        field_value = ValueExpression(act)
        
        # Store the field in the object
        data[field_name] = field_value
        
        # Expect a comma or '}' to end the field definition
        if Look() == ',':
            Take()
        elif Look() == '}':
            Take()
            break
        else:
            Error("Expected ',' or '}' after field value")

    return type_name, data  # Return the type and the parsed fields as a dictionary

def ValueExpression(act):
    # This handles the value for fields (could be a string, number, or other)
    # Example: string, number, etc.
    if Look() == '"':
        return StringExpression(act)  # Call your existing StringExpression if it's a string
    elif Look().isdigit():  # Simple number check (could be expanded for more types)
        return MathExpression(act)  # Assuming the value is a number
    else:
        Error("Unsupported value type")

def Expression(act):
    global pc
    copypc = pc
    ident = TakeNextAlNum()
    # scan for identifier or "str"
    pc = copypc
    if Next() == '\"' or (ident in variables and variables[ident][0] == 's'):
        return ('s', StringExpression(act))
    elif ident in variables and variables[ident][0] == 'd':
        return ('d', DataExpression(act))
    else:
        return ('i', MathExpression(act))


def ParseWhile(act):
    global pc
    local = [act[0]]
    # save PC of the while statement
    pc_while = pc
    while BooleanExpression(local):
        Block(local)
        pc = pc_while
    # scan over inactive block and leave while
    Block([False])


def ParseIf(act):
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

def ParseElseIf(act):
    b = BooleanExpression(act)
    if act[0] and not b:
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


param_count = 0


def ParseCallExpr(act):
    global pc
    # 1) read the function name
    ident = TakeNextAlNum()
    if ident not in variables or variables[ident][0] != 'p':
        Error(f"unknown function '{ident}'")

    # unpack the stored function info
    _, func_pc, func_params = variables[ident]
    param_names = list(func_params.keys())

    # 2) parse *all* of the call-site arguments as full Expressions
    args = []
    if not TakeNext("("):
        Error("missing '(' after function name")
    if not TakeNext(")"):
        # there is at least one argument
        while True:
            arg = Expression(act)
            args.append(arg)
            if TakeNext(")"):
                break
            if not TakeNext(","):
                Error("missing ',' between arguments")

    # 3) arity check
    if len(args) != len(param_names):
        Error(f"'{ident}' expects {len(param_names)} args, got {len(args)}")

    # 4) bind them into variables, saving any old values so we can restore
    old_bindings = {}
    for name, val in zip(param_names, args):
        if name in variables:
            old_bindings[name] = variables[name]
        variables[name] = val

    # 5) jump into the function body
    ret_pc = pc
    pc = func_pc
    Block(act)

    # 6) come back here
    pc = ret_pc

    # 7) restore the caller’s variables
    for name in param_names:
        if name in old_bindings:
            variables[name] = old_bindings[name]
        else:
            del variables[name]


def ParseImport(act):
    e = Expression(act)

    if e[1] in modules:
        variables['m'] = e


def ParseDataDecl(act):
    global pc

    ident = TakeNextAlNum()

    data = {}

    variables[ident] = ('d', pc, data)

    ret_pc = pc
    pc = ret_pc
    Block(act)

    data.update(variables)
 


def ParseFuncDecl():
    global pc, param_count

    ident = TakeNextAlNum()
    params = {}

    if ident == "":
        Error("missing function identifier")

    if TakeNext("("):
        param1 = TakeNextAlNum()
        if param1 != "":
            param_count += 1
            if TakeNext(":"):
                value = ""
                if IsDigit(source[pc]):
                    while IsDigit(source[pc]):
                        value += source[pc]
                        pc += 1
                    params[param1] = ('s', value)
                elif source[pc] == '"':
                    pc += 1
                    while source[pc] != '"':
                        value += source[pc]
                        pc += 1
                    pc += 1

                    params[param1] = ('s', value)
            else:
                params[param1] = ('s', '')

        if TakeNext(','):
            param2 = TakeNextAlNum()
            param_count += 1

            if TakeNext(":"):
                value = ""
                while len(source) < 0 and source[pc].isdigit():
                    value += source[pc]
                print(value)
                params[param2] = ('s', Next())

            params[param2] = ('s', '')

    if not TakeNext(")"):
        Error("missing ')'")

    variables[ident] = ('p', pc, params)
    Block([False])


def ParseAssignment(act):
    ident = TakeNextAlNum()

    if not TakeNext('=') or ident == "":
        Error("unknown statement")

    e = Expression(act)

    if e[1] == "false":
        return 1
    elif e[1] == "true":
        return 0

    if act[0] or ident not in variables:
        # assert initialization even if block is inactive
        variables[ident] = e


def DoReturn(act):
    ident = TakeNextAlNum()
    e = Expression(act)
    if act[0] or ident not in variables:
        variables[ident] = e


def ParseExec(act):
    ident = TakeNextAlNum()

    e = Expression(act)

    os.system(e[1])

    if act[0] or ident not in variables:
        variables[ident] = e


def ParseBreak(act):
    if act[0]:
        # switch off execution within enclosing loop (while, ...)
        act[0] = False


def ParsePrint(act):
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


def ParseRead(act):
    ident = TakeNextAlNum()

    f1 = Expression(act)
    e = Expression(act)

    with open(f1[1], "r") as f:
        if e is not None:
            print(f.read(e[1]))
        else:
            print(f.read())

    if act[0] or ident not in variables:
        variables[ident] = e


def ParseWrite(act):
    ident = TakeNextAlNum()

    e = Expression(act)
    fi = Expression(act)

    with open(e[1], "w+") as f:
        f.write(fi[1])

    if act[0] or ident not in variables:
        variables[ident] = e


def ParseRaise(act):
    # process comma-separated arguments
    while True:
        e = Expression(act)
        if act[0]:
            print(f"{e[1]}")
            exit(1)
        # if not TakeNext(','):
        #     return


def ParseInc(act):
    ident = TakeNextAlNum()
    print(ident)

    e = Expression(act)
    e2 = list(e)

    n = e2.pop()
    n += 1
    e2.append(n)

    if act[0] or ident not in variables:
        variables[ident] = (e[0], e[1])



def RequireParens(name, func, act):
    if not TakeNext('('):
        Error(f"missing '(' after {name}")

    func(act)

    if not TakeNext(')'):
        Error(f"missing ')' after {name}")


def Statement(act):
    if debug:
        print(variables)
    if TakeString("print"):
        RequireParens("print", ParsePrint, act)
    elif TakeString("inc"):
        RequireParens("inc", ParseInc, act)
    elif TakeString("exec"):
        RequireParens("exec", ParseExec, act)
    elif TakeString("raise"):
        RequireParens("raise", ParseRaise, act)
    elif TakeString("break"):
        ParseBreak(act)
    elif TakeString("read"):
        RequireParens("read", ParseRead, act)
    elif TakeString("write"):
        RequireParens("write", ParseWrite, act)
    elif TakeString("if"):
        ParseIf(act)
    elif TakeString("elseif"):
        ParseElseIf(act)
    elif TakeString("while"):
        ParseWhile(act)
    elif TakeString("proc"):
        ParseFuncDecl()
    elif TakeString("data"):
        ParseDataDecl(act)
    elif TakeString("inv"):
        ParseCallExpr(act)
    elif TakeString("using"):
        ParseImport(act)
    else:
        ParseAssignment(act)


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
    s = source[:pc].rfind("\n") + 1
    e = source.find("\n", pc)
    print("[ERROR] " + text + " in line " +
          str(source[:pc].count("\n") + 1) +
          ": '" + source[s:pc] + "_" + source[pc:e] + "'\n")
    sys.exit(1)


# --------------------------------------------------------------------------------------------------


pc = 0
# program couter, identifier -> (type, value) lookup table
variables = {}
file = sys.argv[1]

if len(sys.argv) < 2:
    print("Usage: mince [options] [file]")
    print("No arguments provided!")
    exit(1)

if sys.argv[1].startswith("-"):
    if sys.argv[1].endswith('d'):
        file = sys.argv[2]
        debug = True
else:
    file = sys.argv[1]
try:
    f = open(file, 'r')

except FileNotFoundError:
    print("ERROR: Can't find source file \'" + sys.argv[1] + "\'.")
    sys.exit(1)


# append a null termination
source = f.read() + '\0'


f.close()

Program()
