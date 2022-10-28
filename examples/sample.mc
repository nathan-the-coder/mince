# define the function hello
define hello {
  println! "Hello World"
}

# define the main function (not needed but why not :)
define main {
  println "Hello?"
  # you can only run math expression using print! or println!
  println 1 + 1
  # it will complain if run directly like this:
  # 1 + 1 -> unknown statement _1 + 1

  # you can run a function inside a function
  call hello
}


# call the main function
call main

