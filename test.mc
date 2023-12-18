use "std"
// define the main function
define hello(x, y) { 
    echo "This is the parent function\n"
    echo x, "\n"
    echo "This is y: ", y, "\n"
}

define loop() {
  x = 3
  echo x, "\n"
}

call hello(x:"Hello world", y:1)
call loop()
