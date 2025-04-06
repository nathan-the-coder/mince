use "std"
// define the main function
define hello(x, y) { 
    print("This is the parent function")
    print(x)
    print("This is y: ${y}")
}

define loop() {
  x = 3
  print(x)
}

call hello("Hello world", 1)
call loop()
