#!/usr/bin/env mince

println! "Demo for system module - Running on system.mc"

println! "Running sample.mc\n"
system "mince sample.mc"

println! "Running write.mc"
system "mince write.mc"

println! "Running read.mc"
system "mince read.mc"

println! "removing written file/s"
system "rm test.py"

println! "Running print.mc"
system "mince print.mc"
