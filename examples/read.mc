println! "test.py contents:\n"  # print the string with newline at the end

# read the file with a specific size,
# the value -1 will read all the content of the file
# return an error if file does not exists
read "test.py" -1  

# the read/write function will run twice if inside a function
# define main {
#   read "test.py" -1 
#   write "test.py" "Hello World"
# }
# call main
