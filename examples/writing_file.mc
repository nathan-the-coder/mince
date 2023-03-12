
# run's twice on functions
write "test.mc" 
      "
def main {
i = 1
println i
}

inv main
      "
