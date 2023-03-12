#!/usr/bin/env mince

# it will run twice on function than standalone
read("test_read_file.mc", 100); # read <file_to_read> <bytes_to_read>

# used to stop it running twice on functions
#panic "this will run twice if not by this statement"
