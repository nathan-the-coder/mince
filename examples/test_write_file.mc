
defun test
{

  write "test.mc" 
"
defun main {
  i : 1
  print i
}

inv main
"
}


inv test
