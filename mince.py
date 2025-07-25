#!/usr/bin/env python3
from os import system
from sys import argv
import operator
from value import BaseValue, IntValue, FloatValue, StringValue, FunctionValue
from exception import ReturnException

# VARIABLES:
pc = 0
variable = {}
mince_args = argv


class Interpreter:
    def __init__(self, source: str) -> None:
        self.source = source
        self.pc = 0
        # self.variables = {}
        self.ignored_chars = [' ', '\r', '\n', '\t']
        self.scope = "global"
        self.scopes = [{}]
        self.hadError = False

        self.call_stack = []

    @property
    def variables(self):
        return self.scopes[-1]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def get_variable(self, name):
        for i, scope in enumerate(reversed(self.scopes)):
            if name in scope:
                val = scope[name]
                return val
        self.Error(f"Undefined variable '{name}'")

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
    def TakeNextAlNum(self) -> str:
        alnum = ""
        if self.Next().isalpha():
            while self.pc < len(self.source) and self.Look().isalnum():
                alnum += self.Take()
        return alnum

    # --------------------------------------------------------------------------------------------------
    def BooleanFactor(self, act: list[bool]) -> bool:
        inv = self.TakeNext('!')
        e = self.Expression(act)
        b = e.value
        # skip the white-spaces
        self.Next()
        # a single mathexpression may also serve as a boolean factor
        if (e.type_name == 'i'):
            # Extensively allows comparing numbers
            if self.TakeString("=="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(
                        right, (int, float)):
                    b = (b == right)
                else:
                    self.Error("Invalid types for '==' comparison")
            if self.TakeString("!="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(
                        right, (int, float)):
                    b = (b != right)
                else:
                    self.Error("Invalid types for '!=' comparison")
            if self.TakeString("<="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(
                        right, (int, float)):
                    b = (b <= right)
                else:
                    self.Error("Invalid types for '<=' comparison")

            if self.TakeString(">="):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(
                        right, (int, float)):
                    b = (b >= right)
                else:
                    self.Error("Invalid types for '>=' comparison")

            if self.TakeString(">"):
                right = self.MathExpression(act)
                if isinstance(b, (int, float)) and isinstance(
                        right, (int, float)):
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
                self.Error("Missed symbol ')'")
        elif self.Next().isdigit():
            while self.Look().isdigit():
                left = 10 * left + ord(self.Take()) - ord('0')
        else:
            ident = self.TakeNextAlNum()
            # If the ident is not inside the symbol table,
            if not ident:
                self.Error("expected a name")

            value = self.get_variable(ident)
            if isinstance(value, FunctionValue):
                rtype, value = self.DoCallFun(act, ident)
                return value

            elif not isinstance(value, tuple) and value[0] != 'i':
                self.Error(f"Undefined global {ident}")
            if act[0]:
                left = value[1]
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
        if c == '-':
            left = -left
        # While the next token is a + and - sign,
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
        if self.TakeNext('\"'):
            while not self.TakeString("\""):
                if self.Look() == '\0':
                    self.Error("unexpected EOF")
                if self.TakeString("\\n"):
                    s += '\n'
                if self.TakeString("\\t"):
                    s += '\t'
                else:
                    s += self.Take()
        else:
            ident = self.TakeNextAlNum()

            value = self.get_variable(ident)
            if value[0] == 's':
                s = value[1]
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

    def Expression(self, act) -> BaseValue:
        copypc = self.pc

        # If the next token is a string literal
        if self.Next() == '"':
            return StringValue(self.StringExpression(act))

        # If the next token is a digit, parse as a number
        if self.Next().isdigit():
            expr = self.MathExpression(act)
            if isinstance(expr, int):
                return IntValue(expr)
            elif isinstance(expr, float):
                return FloatValue(expr)

        # If the next token is an identifier, check if it's a string variable
        ident = self.TakeNextAlNum()
        if ident:
            val = self.get_variable(ident)
            # Check for function call
            if isinstance(val, FunctionValue):
                rtype, result = self.DoCallFun(act, ident)
                # Wrap result in appropriate BaseValue subclass
                if rtype == "i":
                    return IntValue(result)
                elif rtype == "s":
                    return StringValue(str(result))
                else:
                    self.Error(f"Unknown return type '{rtype}'")
            else:
                return val

        self.pc = copypc
        # If not a string, digit, or identifier, treat as number expression
        expr = self.MathExpression(act)
        return IntValue(expr) if isinstance(expr, int) else FloatValue(expr)

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
            # process if block?
            if act[0] and not b:
                self.Block(act)
            else:
                self.Block([False])

    def DoCallFun(self, act, ident=""):

        if not self.TakeNext('('):
            self.Error("Missed '(' symbol.")

        ret = self.pc

        func = self.get_variable(ident)
        self.pc = func.block_start
        value = 0

        self.push_scope()

        try:
            self.Block(act)
        except ReturnException as re:
            value = re.value

        self.pop_scope()

        self.pc = ret

        if not self.TakeNext(')'):
            self.Error("Missed ')' symbol.")

        rtype = "s" if isinstance(func.return_value, str) else "i"
        return (rtype, value)

    def DoFunDef(self, act):
        ident = self.TakeNextAlNum()

        if ident == "":
            self.Error("<name> expected.")

        if not self.TakeNext("("):
            self.Error("Missed symbol '('")

        # TODO: Parse parameters here....

        if not self.TakeNext(")"):
            self.Error("Missed symbol ')'")

        if self.Next() != "{":
            self.Error("Missed symbol '{'")

        block_start = self.pc - 1  # position of '{'

        self.variables[ident] = FunctionValue(ident, block_start)
        self.call_stack.append(ident)
        self.Block([False])

    def DoAssign(self, act):
        ident = self.TakeNextAlNum()
        if not self.TakeNext("=") or ident == "":
            self.Error("<expr> expected")

        if act[0]:
            val = self.Expression(act)
            self.variables[ident] = val
        else:
            # still evaluates expr to preserve parser state, but discard result
            _ = self.Expression([False])
            self.variables[ident] = IntValue(0)

    def DoReturn(self, act):
        e = self.Expression(act)
        if act[0]:
            raise ReturnException(e.value)

    def DoRun(self, act):
        # ident = self.TakeNextAlNum()

        e = self.Expression(act)

        system(e.value if isinstance(e.value, str) else "")

        # if act[0] or ident not in variable:
        #     variable[ident] = e

    def DoBreak(self, act):
        if self.scope == "loop":
            if act[0]:
                # switch off execution within enclosing loop (while, ...)
                act[0] = False
        else:
            self.Error("<break> not inside a loop")

    def DoPrint(self, act):
        # process comma-separated arguments
        while True:

            if not self.TakeString("("):
                self.Error("Missed symbol '('")

            e = self.Expression(act)

            if not self.TakeString(")"):
                self.Error("Missed symbol ')'")

            if act[0]:
                print(f"{e.value}")
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
            v = ""
            for sym in symbols.keys():
                if self.TakeString(sym):
                    c = self.Next()
                    value = self.get_variable(ident)
                    v = symbols[sym](value[1], int(c))
            self.variables[ident] = (variable[ident][0], v)

    def DoError(self, act):
        e, line = self.Expression(act), str(self.source[:self.pc].count("\n"))

        try:
            if isinstance(e.value, str):
                print(f"mince: {str(line)}: {e.value}")
            exit(1)
        except TypeError as e:
            raise e

        # if act[0] or ident not in variable:
        #     variable[ident] = e

    def GetMinimum(self, act):
        value = [self.Expression(act).value for _ in range(5)]

        res = min(value)

        self.variables["min"] = IntValue(res)

    def GetMaximum(self, act):

        value = [self.Expression(act).value for _ in range(5)]

        res = max(value)

        self.variables["max"] = IntValue(res)

    def Statement(self, act):
        self.Next()
        if self.pc >= len(self.source) or self.source[self.pc] == '\0':
            return  # Safely skip EOF

        keywords = {
            "let": self.DoAssign,
            "fnc": self.DoFunDef,
            "if": self.DoIfElse,
            "while": self.DoWhile,
            "break": self.DoBreak,
            "return": self.DoReturn,
            "out": self.DoPrint,
            "fail": self.DoError,
            "max": self.GetMaximum,
            "min": self.GetMinimum,
            "exec": self.DoRun,
        }

        if self.Next() in self.ignored_chars:
            return

        ident = self.TakeNextAlNum()

        if ident == "":
            # no identifier, possibly some other statement, handle or error
            self.Error("Expected statement or identifier")

        # Handle keywords
        if ident in keywords:
            keywords[ident](act)
            return
        else:

            # After keywords, check if it's a function call (next char is '(')
            if self.Next() == '(':
                val = self.get_variable(ident)
                if isinstance(val, FunctionValue):
                    self.DoCallFun(act, ident)
                    return
                else:
                    self.Error(f"'{ident}' is not a function")

        # If not keyword or function call, error
        self.Error(f"Unexpected statement or expression: {ident}")

    def Block(self, act):
        if self.TakeNext("{"):
            while not self.TakeNext("}"):
                self.Statement(act)
        else:
            self.Statement(act)

    def Error(self, text: str):
        s, e = self.source[:self.pc].rfind(
            "\n") + 1, self.source.find("\n", self.pc)

        if e == -1:  # No newline after PC
            e = len(self.source)

        msg = ("mince:" + mince_args[1] + ":" +
               str(self.source[:self.pc].count("\n")+1) + ": " +
               text + " near " + "\n\t'" + self.source[s:self.pc] +
               "_" + self.source[self.pc:e] + "'")

        self.hadError = True
        print(msg)
        exit(1)

    def run(self):
        act = [True]
        while self.pc < len(self.source):
            self.Next()
            if self.source[self.pc] == '\0':
                break
            self.Block(act)


def runFile(interp, path: str):
    try:

        f = open(path, 'r')
        interp.source = f.read() + '\0'

        f.close()
    except FileNotFoundError:
        print("ERROR: Can't find source file \'" + path + "\'.")
        exit(1)
    interp.run()


if __name__ == '__main__':
    interp = Interpreter("")
    if len(mince_args) < 2:
        print("No arguments provided.")
        print("Example usage: ./mince.py <file>")
    else:
        runFile(interp, argv[1])
