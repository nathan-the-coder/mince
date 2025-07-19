
fnc test() {
  print("outer")

  fnc test1() {
    print("inner")
  }

  call test1
}

call test
