#!/usr/bin/env python3
from os import system
from sys import argv
import re
import operator

# VARIABLES:
pc = 0
variable = {}
mince_args = argv


ExprValue = str | int | float
class Interpreter:
    def __init__(self, source: str) -> None:
        self.source = source
        self.pc = 0
        self.variables = {}
        self.ignored_chars = [' ', '\r', '\n', '\t' ]
        self.scope = "global"
        self.on_repl = True
        self.hadError = False

        self.types = {
            "s": "string", "i": "int", "f": "float", "b": "bool", "fn": "function"
        }

    # returns the current character while skipping over comments
    def Look(self) -> str:
        # comments are entered by # and exited by \n or \0

        if self.pc < len(self.source) and self.source[self.pc] == '#':
            while self.pc < len(self.source) and self.source[self.pc] != '\n' and self.source[self.pc+1] != '\0':
                # scan over comments here
                self.pc += 1
        return self.source[self.pc]

    # takes away and returns the current character
    def Take(self) -> str:
        c = self.Look()
        self.pc += 1
        return c

    # returns whether a certain string could be taken starting at pc
    def TakeString(self, word: str) -> bool:
        copypc = self.pc
        for c in word:
            if self.Take() != c:
                self.pc = copypc
                return False
        return True

    # returns the next non-whitespace character
    def Next(self) -> str:
        while self.pc < len(self.source) and self.source[self.pc] in self.ignored_chars:
            self.pc += 1
        return self.source[self.pc] if self.pc < len(self.source) else '\0'

    # eats white-spaces, returns whether a certain character could be eaten
    def TakeNext(self, c) -> bool:
        if self.Next() == c:
            self.Take()
            return True
        else:
            return False


    # recognizers
    def IsAddOp(self, c: str) -> bool: return (c == '+' or c == '-')
    def IsMulOp(self, c: str) -> bool: return (c == '*' or c == '/')

    # Takes the next alpha numeric character 
    # checks if the next token is a alpha, 
    # while the current token isnt a symbol, take it and increment the return by what taken
    def TakeNextAlNum(self) -> str:
        alnum = ""
        if self.Next().isalpha():
            while self.pc < len(self.source) and self.Look().isalnum():
                alnum += self.Take()
        return alnum

    # --------------------------------------------------------------------------------------------------

    def LookupType(self, type_alias: str): 
        return self.types[type_alias]

    def BooleanFactor(self, act: list[bool]) -> bool:
        inv = self.TakeNext('!')
        e = self.Expression(act)
        b = e[1]
        # skip the white-spaces
        self.Next()
        # a single mathexpression may also serve as a boolean factor
        if (e[0] == 'i'):
            # Extensively allows comparing numbers
            if self.TakeString("=="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(right, (int, float)):
                    b = (b == right)
                else:
                    self.Error("Invalid types for '==' comparison")
            if self.TakeString("!="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(right, (int, float)):
                    b = (b != right)
                else:
                    self.Error("Invalid types for '!=' comparison")
            if self.TakeString("<="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(right, (int, float)):
                    b = (b <= right)
                else:
                    self.Error("Invalid types for '<=' comparison")

            if self.TakeString(">="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(right, (int, float)):
                    b = (b >= right)
                else:
                    self.Error("Invalid types for '>=' comparison")

            if self.TakeString(">"):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(right, (int, float)):
                    b = (b > right)
                else:
                    self.Error("Invalid types for '>' comparison")
        else:
            # Allows comparison between strings
            if self.TakeString("=="):
                b = (b == self.StringExpression(act))
            if self.TakeString("!="):
                b = (b != self.StringExpression(act))
            else:
                b = (b != "")
        # always returns False if inactive
        return act[0] and (b != inv)


    def BooleanTerm(self, act: list[bool]) -> bool:
        b = self.BooleanFactor(act)
        # Checks for the `and` logic operator and 
        # pass the logics into the BooleanFactor for strings and numbers.
        while self.TakeString('&&'):
            # logical and corresponds to multiplication
            b = b & self.BooleanFactor(act)
        return b


    def BooleanExpression(self, act) -> bool:
        b = self.BooleanTerm(act)
        # Checks for the `or` logic operator and 
        # pass the logics into the BooleanFactor for strings and numbers.
        while self.TakeString('||'):
            # logical or corresponds to addition
            b = b | self.BooleanTerm(act)
        return b


    def MathFactor(self, act) -> int | float:
        left = 0
        # Check for higher precedence parenthesis first before other operators
        # and parse the math Expression inside first.
        if self.TakeNext('('):
            left = self.MathExpression(act)
            if not self.TakeNext(')'):
                self.Error("missing ')'")
        if self.Next().isdigit():
            # While the current token is digit increment the `m` variable and making sure 
            # it aligns well with base10 and by converting the taken token value into python integer,
            # and adding them to `m` while also converting it to a `real` integer from `ascii`
            while self.Look().isdigit():
                left = 10 * left + ord(self.Take()) - ord('0')
        else:
            ident = self.TakeNextAlNum()
            # If the ident is not inside the symbol table,
            # or if the variable named by the value of `ident` type is not of number,
            # returns an error using the intepreters main error handler. 
            if not ident:
                self.Error("expected a name")

            if ident not in self.variables or self.variables[ident][0] != 'i':
                self.Error("unknown variable")
            if act[0]:
                # asign the left value to the value of the variable of the name inside of ident
                left = self.variables[ident][1]
        return left


    def MathTerm(self, act) -> int | float:
        # Get the left token value from mathfactor
        left = self.MathFactor(act)
        while self.IsMulOp(self.Next()):
            c = self.Take()
            right = self.MathFactor(act)
            if c == '*':
                # multiplication
                left = left * right
            else:
                # division
                left = left / right
        return left


    def MathExpression(self, act) -> int | float:
        # check for an optional leading sign
        c = self.Next()
        if self.IsAddOp(c):
            # Take the next value and assign it to `c`
            # this checks for leading sign that could be `negation`
            c = self.Take()

        # Get the left token value
        left = self.MathTerm(act)
        # If the leading is minus, negate the left token value and assign it as the new value of the left token
        if c == '-':
            left = -left
        # While the next token is a + and - sign,
        # take the next token apart from the previous token, and assign it to `c` as the operator
        # then get the right hand side value
        # Do calculations in each sign by adding or subtracting the value of `left` token and `right` token
        while self.IsAddOp(self.Next()):
            c = self.Take()
            right = self.MathTerm(act)
            if c == '+':
                # addition
                left = left + right
            else:
                # subtraction
                left = left - right
        return left


    def String(self, act: list[bool]) -> str:
        s = ""
        # is it a literal string?
        # Check if the next token is a '"'
        if self.TakeNext('\"'):
            # While the next token isn't a '"', parse it and increment the `s` as it needs to,
            # or returns an error if it can't find the last '"'.
            while not self.TakeString("\""):
                if self.Look() == '\0':
                    # If it finds a null terminator already, then return a error about the unexpected eof.
                    self.Error("unexpected EOF")
                if self.TakeString("\\n"):
                    # if the next token is a newline character, add the symbol '\n' to the return `s` variable 
                    s += '\n'
                if self.TakeString("\\t"):
                    # if the next token is a tab character, add the symbol '\t' to the return `s` variable 
                    s += '\t'
                else:
                    # if the next token is not a newline, tab, or an eof, take the next token and add it to the `s` value
                    s += self.Take()
        else:
            # if it isn't a literal string, get the identifier from the lexer.
            ident = self.TakeNextAlNum()

            # then check if the identifier found is in the symbol table, 
            # and if the type of the identifier is a string,
            if ident in self.variables and self.variables[ident][0] == 's':
                # if so then assign the value of the identifier to the `s` variable return.
                s = self.variables[ident][1]
            else:
                # else returns an error that it isn't a string.
                self.Error("not a string")

        return s


    def StringExpression(self, act: list[bool]) -> str:
        s = self.String(act)
        while self.TakeNext('+'):
            # string addition = concatenation
            s += self.String(act)
        return s

    

    def Expression(self, act) -> tuple[str, ExprValue]:
        copypc = self.pc

        ident = self.TakeNextAlNum()

        # scan for identifier
        self.pc = copypc
        
        # if the next token is a string literal, or 
        # if the identifier is a string type variable
        # return the respective symbol for string an integer, 
        if(self.Next() == '\"' or (ident in self.variables and self.variables[ident][0] == 's')):
            # return a symbol that corresponds to String Node
            return ("s", self.StringExpression(act))
        else:
            # if it isn't a string literal, then return a number symbol using the MathExpression return value as the value of the symbol
            return ("i", self.MathExpression(act))

    def DoWhile(self, act):
        local = [act[0]]

        # save PC of the while statement
        pc_while = self.pc

        while self.BooleanExpression(local):
            self.Block(local)
            self.pc = pc_while

        # scan over inactive block and leave while
        self.Block([False])

    def DoIfElse(self, act):
        b = self.BooleanExpression(act)

        if act[0] and b:
            # process if block?
            self.Block(act)
        else:
            self.Block([False])

        self.Next()

        # process else block?
        if self.TakeString("else"):
            if act[0] and not b:
                self.Block(act)
            else:
                self.Block([False])


    def DoCallFun(self, act):
        ident = self.TakeNextAlNum()

        print(ident, self.variables[ident])
        if ident not in self.variables or self.variables[ident][0] != 'fn':
            self.Error("unknown function")

        ret = self.pc
        self.pc = self.variables[ident][1]
        print(f"self.variables: {self.variables}, self.pc: {self.pc}, ret: {ret}")
        self.Block(act)

        # execute block as a subroutine
        self.pc = ret

    def ExecFun(self, ident, act):
        ret = self.pc
        self.pc = self.variables[ident][1]
        print(self.variables)
        self.Block(act)

        # execute block as a subroutine
        self.pc = ret

    def match(self, value, char):
        global pc
        while re.match(r'[a-zA-Z]', char):
            value += char
            pc += 1
            char = self.source[self.pc]
        return value

    def newValue(self, value, char):
        global pc
        pc += 2
        value2 = self.match(value, char)
        return value2

    def DoFunDef(self, act):
        ident = self.TakeNextAlNum()

        if ident == "":
            self.Error("missing function identifier")
        
        if self.Next() != "{":
            self.Error("missing '{' after function definition")

        block_start = self.pc - 1  # position of '{'
        self.variables[ident] = ('fn', block_start)
        self.Block([False])

    def DoAssign(self, act):
        # Get the assignee name for the variable 
        ident = self.TakeNextAlNum()

        # Checks if the ident is empty or the next char isnt '=', as it is expects, if it is not so then return an error.
        if not self.TakeNext("=") or ident == "":
            self.Error("unknown statement")

        # parse new expression after assign 
        e = self.Expression(act)

        if act[0] or ident not in self.variables:
            # assert initialization even if block is inactive
            # while re.match(r'[0-9]', varia)
            self.variables[ident] = e
        
    def DoReturn(self, act):
        ident = self.TakeNextAlNum()
        e = self.Expression(act)
        if self.scope == "function":
            if act[0] or ident not in self.variables:
                variable[ident] = e
        else:
            self.Error("Illegal `return` outside of function")

    def DoRun(self, act):
        # ident = self.TakeNextAlNum()

        e = self.Expression(act)

        system(e[1] if isinstance(e[1], str) else "")

        # if act[0] or ident not in variable:
        #     variable[ident] = e


    def DoBreak(self, act):
        if self.scope == "loop":
            if act[0]:
                # switch off execution within enclosing loop (while, ...)
                act[0] = False
        else:
            self.Error("Illegal `break` outside of loop")


    def DoPrint(self, act):
        # process comma-separated arguments
        while True:

            if not self.TakeString("("):
                self.Error("Missing '(' after 'print'")
                

            e = self.Expression(act)

            if not self.TakeString(")"):
                self.Error("Missing ')' after expression")

            if act[0]:
                print(f"{self.LookupType(e[0])}:   {e[1]}")
            if not self.TakeNext(','):
                return


    def IDMD(self):
        ident = self.TakeNextAlNum()

        self.Next()

        symbols = {
                "+=": lambda a, b: operator.iadd(a, b),
                "-=": lambda a, b: operator.isub(a, b),
                "*=": lambda a, b: operator.imul(a, b),
                "/=": lambda a, b: operator.ifloordiv(a, b),
                "%=": lambda a, b: operator.imod(a, b),
                }

        if ident != "":
            val = ""
            for sym in symbols.keys():
                if self.TakeString(sym):
                    c = self.Next()
                    val = symbols[sym](self.variables[ident][1], int(c))
            self.variables[ident] = (variable[ident][0], val)

    def DoError(self, act):
        e, line = self.Expression(act), str(self.source[:self.pc].count("\n"))

        try:
            if isinstance(e[1], str):
                print(f"mince: " + ":" + str(line) + ":" + " " + e[1])
            exit(1)
        except TypeError as e:
            raise e

        # if act[0] or ident not in variable:
        #     variable[ident] = e

    def GetMinimum(self, act):
        value = [self.Expression(act) for _ in range(5)]

        res = min(value)

        variable["min"] = ('i', res)

    def GetMaximum(self, act):

        value = [self.Expression(act) for _ in range(5)]

        res = max(value)

        variable["max"] = ('i', res)

    def Statement(self, act):

        keywords = {
                "min":      self.GetMinimum,
                "max":      self.GetMaximum,
                "print":    self.DoPrint,
                "return":   self.DoReturn,
                "exec":     self.DoRun,
                "panic":    self.DoError,

                "if":       self.DoIfElse,
                "while":    self.DoWhile,
                "break":    self.DoBreak,

                "call":     self.DoCallFun,
                "fnc":      self.DoFunDef,
                "let":      self.DoAssign,
                }

            
        # Skip ignored characters
        if self.Next() in self.ignored_chars:
            return

        # Get the next token without consuming it
        # Direct dictionary lookup 
        ident = self.TakeNextAlNum()
        if ident in keywords:
            keywords[ident](act)
            return
        elif ident in self.variables and self.variables[ident][0] == 'fn':
            print(ident)
            self.ExecFun(ident, act)

        self.Error("Unknown statement or token")


    def Block(self, act):
        if self.TakeNext("{"):
            while not self.TakeNext("}"):
                self.Block(act)
        else:
            self.Statement(act)


    def Error(self, text: str):
        s, e = self.source[:self.pc].rfind("\n") + 1, self.source.find("\n", self.pc)

        itype = mince_args[1] if not self.on_repl else "stdin"
        msg = ("mince:" + itype + ":" +
            str(self.source[:self.pc].count("\n")+1) + ": " +
            text + " near " + "\n\t'" + self.source[s:self.pc] +
            "_" + self.source[self.pc:e] + "'")

        self.hadError = True
        if not self.on_repl:
            print(msg)
            exit(1)
        else:
            raise RuntimeError(msg)

def run(interp: Interpreter):
    act = [True]
    while interp.Next() != '\0':
        interp.Block(act)

def runPrompt(interp: Interpreter):
    while True:
        try:
            source = input("mince > ")
            # Parse repl commands (outside of tokens)
            if source.startswith(";"):
                command = source.strip(";")
                match command:
                    case "exit":
                        break
                    case "help":
                        print("TODO: Implement repl help menu")
                    case _:
                        print(f"Unrecognized repl command found: '{command}'")
                        break
            else:
                interp.source = source + '\n'
                interp.pc = len(interp.source) - len(source) - 1 # Staart of the new input
                interp.on_repl = True
                # Start the interpreter
                try:
                    run(interp)
                except Exception as e:
                    print(e.args[0] if hasattr(e, 'args') and e.args else str(e))

        except KeyboardInterrupt:
            print("\nBye!")
            break



def runFile(interp, path: str):
    try:

        f = open(path, 'r')
        interp.source = f.read() + '\0'
        interp.on_repl = False

        f.close()
    except FileNotFoundError:
        print("ERROR: Can't find source file \'" + path + "\'.")
        exit(1)
    run(interp)

if __name__ == '__main__':
    interp = Interpreter("")
    if len(mince_args) == 1: 
        runPrompt(interp)
    else:
        runFile(interp, argv[1])
