import mince


# OPTIONAL APPROACH:
  # set mince arguments to this file arguments
  #from sys import argv
  #mince.mince_args = argv
  # You can point the source variable in mince to a file in argv[2] or...
  #f = open(argv[2], 'r')
  #mince.source = f.read() + '\0'

# MODULAR APPROACH:
# make the source variable in mince point to a string like:
mince.source = "print(\"Hello world\");\0"
mince.run()
