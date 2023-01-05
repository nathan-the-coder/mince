defun test
  read "test_read_file.mc" 100 # read <file_to_read> <bytes_to_read>
  panic "this will run twice if not by this statement"
end

inv test
