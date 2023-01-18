#!/usr/bin/env mince
defun main
  var = 3
  print "Variable 'var' default value"
  print var

  print "Incrementing var by 3"
  inc "var" "3"
  print var


  print "Decrementing var by 1"
  dec "var" "1"
  print var
end


inv main
