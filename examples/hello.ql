
// TODO: BETTER SYNTAX
DEFINE MAIN { 
  // with newline
  FORMAT "Hello World" 

  // without newline
  OUTPUT "Hello World"
}

// run the function main
RUN MAIN 

foo=0
bar=1 

test=1

IF test == 1 {
  FORMAT "YES"
}
ELSE {
  OUTPUT "NO"
}
