using "std"

// define the main function
proc hello(x, y) { 
    print("This is the parent function")
    print(x)
    print("This is y: ${y}")
}

proc loop() {
  x = 3
  print(x)
}

inv hello("Hello world", 1)
inv loop()
