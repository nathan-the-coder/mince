
def test {
  write "test.mc" 
        "
def main {
  i = 1
  println i
}

inv main
        "
}


inv test
