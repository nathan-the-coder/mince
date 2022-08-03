#!/usr/bin/env python

import sys, os


if sys.argv[1] == "install":
    print("install -Dm755 ./mince ~//local/bin/")
    os.system("install -Dm755 ./mince ~/local/bin/")

