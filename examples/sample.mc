# define the function print
define print {
  println! "Hello World"
}

# define the main function
define main {
  print! "Hello?\n"
  print! 1 + 1
  goto print
}


# call the main function
goto main

