using "std"

data User {
  name = "current"
  age = 10

  proc greet() {
    print("Hello " + name)
  }
}

proc main() {
  x = 5

  users = User { name: "nathan", age: 21 }
  print(users)

  if x == 10 {
    print(1)
  } elseif x == 5 {
    print(2)
  } else {
    print(3)
  }
}

inv main()
