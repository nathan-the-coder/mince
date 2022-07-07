
DEFINE MAIN {
  MKHTML
  SERVE::INIT

  FORMAT "Init server success at 'localhost:8080'"

  SERVE::RUN
}

RUN MAIN
