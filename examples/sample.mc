use "std"

define hello() {
  echo "Hello World"
}

define main() {
  echo "Hello?"

  call hello()
}
