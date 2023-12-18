-- type: ignore
local modules = { "tk" }
local debug = false
local pc = 1
local source = ""
-- program counter, identifier -> (type, value) lookup table
local variables = {}

-- returns the current character while skipping over comments
function Look()
  -- comments are entered by # and exited by \n or \0
  if pc < #source and source:sub(pc, pc + 1) == "//" then
    while pc <= #source and source:sub(pc, pc) ~= "\n" and source:sub(pc, pc) ~= "\0" do
      -- scan over comments here
      pc = pc + 1
    end
  end
  return source:sub(pc, pc)
end

-- takes away and returns the current character
function Take()
  local c = Look()
  pc = pc + 1
  return c
end

-- returns whether a certain string could be taken starting at pc
function TakeString(word)
  local copypc = pc
  for i = 1, #word do
    if Take() ~= word:sub(i, i) then
      pc = copypc
      return false
    end
  end
  return true
end

-- returns the next non-whitespace character
function Next()
  while Look() == " " or Look() == "\t" or Look() == "\n" or Look() == "\r" do
    Take()
  end
  return Look()
end

-- eats white-spaces, returns whether a certain character could be eaten
function TakeNext(c)
  if Next() == c then
    Take()
    return true
  else
    return false
  end
end

-- recognizers
function IsDigit(c)
  return (c >= '0' and c <= '9')
end

function IsAlpha(c)
  return ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'))
end

function IsAlNum(c)
  return (IsDigit(c) or IsAlpha(c))
end

function IsAddOp(c)
  return (c == '+' or c == '-')
end

function IsMulOp(c)
  return (c == '*' or c == '/')
end

function TakeNextAlNum()
  local alnum = ""
  if IsAlpha(Next()) then
    while IsAlNum(Look()) do
      alnum = alnum .. Take()
    end
  end
  return alnum
end

-- --------------------------------------------------------------------------------------------------

function BooleanFactor(act)
  local inv = TakeNext('!')
  local e = Expression(act)
  local b = e[1]
  Next()
  -- a single mathexpression may also serve as a boolean factor
  if (e[0] == 'i') then
    if TakeString("==") then
      b = (b == MathExpression(act))
    elseif TakeString("!=") then
      b = (b ~= MathExpression(act))
    elseif TakeString("<=") then
      b = (b <= MathExpression(act))
    elseif TakeString("<") then
      b = (b < MathExpression(act))
    elseif TakeString(">=") then
      b = (b >= MathExpression(act))
    elseif TakeString(">") then
      b = (b > MathExpression(act))
    end
  else
    if TakeString("==") then
      b = (b == StringExpression(act))
    elseif TakeString("!=") then
      b = (b ~= StringExpression(act))
    else
      b = (b ~= "")
    end
  end
  -- always returns False if inactive
  return act[1] and (b ~= inv)
end

function BooleanTerm(act)
  local b = BooleanFactor(act)
  while TakeString('and') do
    -- logical and corresponds to multiplication
    b = b and BooleanFactor(act)
  end
  return b
end

function BooleanExpression(act)
  local b = BooleanTerm(act)
  while TakeString('or') do
    -- logical or corresponds to addition
    b = b or BooleanTerm(act)
  end
  return b
end

local function ord(c)
  return string.byte(c)
end

function MathFactor(act)
  local m = 0
  if TakeNext('(') then
    m = MathExpression(act)
    if not TakeNext(')') then
      Error("missing ')'")
    end
  elseif IsDigit(Next()) then
    while IsDigit(Look()) do
      m = 10 * m + ord(Take()) - ord('0')
    end
  elseif TakeString("val(") then
    local s = String(act)
    if act[1] and s:match("^%d+$") then
      m = tonumber(s)
    end
    if not TakeNext(')') then
      error("missing ')'")
    end
  else
    local ident = TakeNextAlNum()
    if not variables[ident] then
      error("unknown variable: " .. ident)
    elseif variables[ident][1] ~= 'i' then
      error("variable '" .. ident .. "' is not a number")
    elseif act[1] then
      m = variables[ident][2]
    end
  end
  return m
end

function MathTerm(act)
  local m = MathFactor(act)
  while IsMulOp(Next()) do
    local c = Take()
    local m2 = MathFactor(act)
    if c == '*' then
      -- multiplication
      m = m * m2
    else
      -- division
      m = m / m2
    end
  end
  return m
end

function MathExpression(act)
  -- check for an optional leading sign
  local c = Next()
  if IsAddOp(c) then
    c = Take()
  end
  local m = MathTerm(act)
  if c == '-' then
    m = -m
  end
  while IsAddOp(Next()) do
    c = Take()
    local m2 = MathTerm(act)
    if c == '+' then
      -- addition
      m = m + m2
    else
      -- subtraction
      m = m - m2
    end
  end
  return m
end

function String(act)
  local s = ""
  -- is it a literal string?
  if TakeNext('"') then
    while not TakeString('"') do
      if Look() == '\0' then
        error("unexpected EOF")
      end
      if TakeString("\\n") then
        s = s .. '\n'
      else
        s = s .. Take()
      end
    end
  else
    local ident = TakeNextAlNum()
    if variables[ident] and variables[ident][1] and variables[ident][1] ~= 'i' then
      s = variables[ident][1]
    else
      error("not a string")
    end
  end
  return s
end

function StringExpression(act)
  local s = String(act)
  while TakeNext('+') do
    -- string addition = concatenation
    s = s .. String(act)
  end
  return s
end

function Expression(act)
  local copypc = pc
  local ident = TakeNextAlNum()
  -- scan for identifier or "str"
  pc = copypc
  if Next() == '"' or (variables[ident] and variables[ident][1] and variables[ident][1] ~= 'i') then
    return { 's', StringExpression(act) }
  else
    return { 'i', MathExpression(act) }
  end
end

function DoFor(act)
  -- Parse initialization expression (variable assignment)
  local ident = TakeNextAlNum()
  if not TakeNext('=') then
    Error("Expected '=' in for loop initialization")
  end
  local initialValue = MathExpression(act)
  variables[ident] = { 'i', initialValue }

  -- Parse condition expression (condition for loop termination)
  if not TakeNext(';') then
    Error("Expected ';' after for loop initialization")
  end
  local condition = BooleanExpression(act)
  print(Take())

  -- Parse increment expression (increment of loop variable)
  if not TakeNext(';') then
    error("Expected ';' after for loop condition")
  end
  local incrementVar = TakeNextAlNum()
  if incrementVar ~= ident then
    error("Increment variable must match loop variable")
  end
  if not TakeNext("+") or not TakeNext("=") then
    error("Expected '+=' in increment expression")
  end
  local increment = MathExpression(act)

  -- Begin for loop execution
  while condition do
    Block(act) -- Execute the loop's block of code

    -- Update loop variable with increment value
    initialValue = initialValue + increment
    variables[ident][2] = initialValue

    -- Check loop condition for termination
    condition = BooleanExpression(act)
  end
end

function DoWhile(act)
  local local_act = { act[1] }
  -- save PC of the while statement
  local pc_while = pc
  while BooleanExpression(local_act) do
    Block(local_act)
    pc = pc_while
  end
  -- scan over inactive block and leave while
  Block({ false })
end

function DoIfElse(act)
  local b = BooleanExpression(act)
  if act[1] and b then
    -- process if block?
    Block(act)
  else
    Block({ false })
  end
  Next()
  if TakeString("elif") then
    if act[1] and not b then
      Block(act)
    elseif not act[1] and b then
      Block({ b })
    else
      Block({ false })
    end
  end
  Next()
  -- process else block?
  if TakeString("else") then
    if act[1] and not b then
      Block(act)
    else
      Block({ false })
    end
  end
end

local param_count = 0

function DoCallFun(act)
  local ident = TakeNextAlNum()
  -- if not (variables[ident] and variables[ident][1] and variables[ident][1] ~= 'p') then
  --   error("unknown function")
  -- end

  if param_count ~= 0 then
    if TakeNext("(") then
      local arg1 = TakeNextAlNum()

      if TakeNext(":") then
        local value = ""

        if IsDigit(source[pc]) then
          while IsDigit(source[pc]) do
            value = value .. source[pc]
            pc = pc + 1
          end
          variables[arg1] = { 's', value }
        elseif source[pc] == '"' then
          pc = pc + 1
          while source[pc] ~= '"' do
            value = value .. source[pc]
            pc = pc + 1
          end
          pc = pc + 1

          variables[arg1] = { 's', value }
        end
      end
    end

    if TakeNext(",") and not TakeNext(')') then
      local arg2 = TakeNextAlNum()

      if TakeNext(":") then
        local value = ""

        if IsDigit(source[pc]) then
          while IsDigit(source[pc]) do
            value = value .. source[pc]
            pc = pc + 1
          end
          variables[arg2] = { 's', value }
        elseif source[pc] == '"' then
          pc = pc + 1
          while source[pc] ~= '"' do
            value = value .. source[pc]
            pc = pc + 1
          end
          pc = pc + 1

          variables[arg2] = { 's', value }
        end
      end
    end
  end

  if not TakeNext(")") then
    error("missing ')'")
  end

  local ret = pc
  pc = variables[ident][2]
  Block(act)
  -- execute block as a subroutine
  pc = ret
end

function DoImport(act)
  local e = Expression(act)

  if e[2] and e[2] == modules then
    variables['m'] = e
  end
end

function DoFunDef()
  local ident = TakeNextAlNum()

  if ident == "" then
    error("missing function identifier")
  end

  if TakeNext("(") then
    local param1 = TakeNextAlNum()
    if param1 ~= "" then
      param_count = param_count + 1
      if TakeNext(":") then
        local value = ""
        if IsDigit(source[pc]) then
          while IsDigit(source[pc]) do
            value = value .. source[pc]
            pc = pc + 1
          end
          variables[param1] = { 's', value }
        elseif source[pc] == '"' then
          pc = pc + 1
          while source[pc] ~= '"' do
            value = value .. source[pc]
            pc = pc + 1
          end
          pc = pc + 1

          variables[param1] = { 's', value }
        else
          variables[param1] = { 's', '' }
        end
      else
        variables[param1] = { 's', '' }
      end
    end

    if TakeNext(',') then
      local param2 = TakeNextAlNum()
      param_count = param_count + 1

      if TakeNext(":") then
        local value = ""
        while #source > 0 and source[pc]:find("%d") do
          value = value .. source[pc]
        end
        variables[param2] = { 's', Next() }
      else
        variables[param2] = { 's', '' }
      end
    end
  end

  if not TakeNext(")") then
    error("missing ')'")
  end

  variables[ident] = { 'p', pc }
  Block({ false })
end

function DoAssign(act)
  local ident = TakeNextAlNum()

  if not TakeNext('=') or ident == "" then
    error("unknown statement")
  end

  local e = Expression(act)

  if e[2] == "false" then
    return 1
  elseif e[2] == "true" then
    return 0
  end

  if act[1] or not variables[ident] then
    -- assert initialization even if block is inactive
    variables[ident] = e
  end
end

function DoReturn(act)
  local ident = TakeNextAlNum()
  local e = Expression(act)
  if act[1] or not variables[ident] then
    variables[ident] = e
  end
end

function DoRun(act)
  local ident = TakeNextAlNum()

  local e = Expression(act)

  os.execute(e[2])

  if act[1] or not variables[ident] then
    variables[ident] = e
  end
end

function DoBreak(act)
  if act[1] then
    -- switch off execution within enclosing loop (while, ...)
    act[1] = false
  end
end

function DoPrint(act)
  -- process comma-separated arguments
  while true do
    local e = Expression(act)
    if act[1] then
      io.write(e[2])
    end
    if not TakeNext(',') then
      return
    end
  end
end

function DoExit(act)
  local e = Expression(act)
  os.exit(e[2])
end

function DoRead(act)
  local ident = TakeNextAlNum()

  local f1 = Expression(act)
  local e = Expression(act)

  local file = io.open(f1[2], "r")
  if file then
    local content = file:read(e[2])
    if content then
      print(content)
    end
    file:close()
  end

  if act[1] or not variables[ident] then
    variables[ident] = e
  end
end

function DoWrite(act)
  local ident = TakeNextAlNum()

  local e = Expression(act)
  local fi = Expression(act)

  local file = io.open(e[2], "w+")
  if file then
    file:write(fi[2])
    file:close()
  end

  if act[1] or not variables[ident] then
    variables[ident] = e
  end
end

function DoError(act)
  -- process comma-separated arguments
  while true do
    local e = Expression(act)
    local line = string.match(string.sub(source, 1, pc), "\n")
    if act[1] then
      print("mince: " .. arg[1] .. ":" .. line .. ": " .. e[2])
      os.exit(1)
    end
    -- if not TakeNext(',') then
    --     return
    -- end
  end
end

function DoIncrement(act)
  local ident = TakeNextAlNum()
  print(ident)

  local e = Expression(act)
  local e2 = { table.unpack(e) }

  local n = table.remove(e2)
  n = n + 1
  table.insert(e2, n)

  if act[1] or not variables[ident] then
    variables[ident] = { e[1], e[2] }
  end
end

function Statement(act)
  if debug then
    print(variables)
  end
  if TakeString("echo") then
    DoPrint(act)
  elseif TakeString("inc") then
    DoIncrement(act)
  elseif TakeString("sh") then
    DoRun(act)
  elseif TakeString("error") then
    DoError(act)
  elseif TakeString("break") then
    DoBreak(act)
  elseif TakeString("read") then
    DoRead(act)
  elseif TakeString("write") then
    DoWrite(act)
  elseif TakeString("if") then
    DoIfElse(act)
  elseif TakeString("while") then
    DoWhile(act)
  elseif TakeString("for") then
    DoFor(act)
  elseif TakeString("call") then
    DoCallFun(act)
  elseif TakeString("define") then
    DoFunDef()
  elseif TakeString("use") then
    DoImport(act)
  else
    DoAssign(act)
  end
end

function Block(act)
  if TakeNext("{") then
    while not TakeNext("}") do
      Block(act)
    end
  else
    Statement(act)
  end
end

function Program()
  local act = { true }
  while Next() ~= '\0' do
    Block(act)
  end
end

function Error(text)
  local s = string.sub(source, 1, pc):find("\n") + 1
  local e = string.find(source, "\n", pc)
  print("[ERROR] " .. text .. " in line " ..
    tostring(string.sub(source, 1, pc):gsub("\n", ""):len() + 1) ..
    ": '" .. string.sub(source, s, pc) .. "_" .. string.sub(source, pc, e) .. "'\n")
  os.exit(1)
end

local file = arg[1]

if #arg < 1 then
  print("Usage: mince [options] [file]")
  print("No arguments provided!")
  os.exit(1)
end

if string.sub(arg[1], 1, 1) == "-" then
  if string.sub(arg[1], -1) == 'd' then
    file = arg[2]
    debug = true
  end
else
  file = arg[1]
end

local f, err = io.open(file, 'r')

if not f then
  print("ERROR: Can't find source file \'" .. arg[1] .. "\'.")
  os.exit(1)
end

-- append a null termination
source = f:read("*a") .. '\0'
f:close()

Program()
