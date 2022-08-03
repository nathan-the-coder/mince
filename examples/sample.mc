# define the function hello
define hello {
  println! "Hello World"
}

# define the main function (not needed but why not :)
define main {
  println! "Hello?"
  println! 1 + 1
  call hello
}


# call the main function
call main

