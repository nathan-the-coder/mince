define print {
  println! "Hello World"
}

define main {
  println! "Hello?"
  println! 1 + 1
  goto print
}


# call the main function
goto main

