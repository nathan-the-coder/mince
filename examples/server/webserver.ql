
DEFINE MAIN %
  MKHTML
  PRINT "Initializing server at 'localhost:8080'\n"
  SERVE::INIT


  SERVE::OPEN
%

RUN MAIN
