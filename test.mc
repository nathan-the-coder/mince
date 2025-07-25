
fnc add() {
  let x = 2
  if x == 2 {
    out(1)
  }
  return 5
}

let test = add()
out(test)

fnc dep() {
  out(1)
}

dep()
