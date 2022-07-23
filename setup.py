#!/usr/bin/env python3

# Import the scripts to be used inside the setup.py
from scripts import log, shop

# Variables to store directories used by the conditionals
localDir = "/home/nathan/.local/"

# check for the python local path if it is 3.10 or 3.9
if os.path.isDir(localDir + "lib/python3.10/site-packages/"):
    pythonDir = localDir + "lib/python3.10/site-packages/"
else:
    pythonDir = localDir + "lib/python3.9/site-packages/"

# snak installation dirs
snak = localDir + 'bin/snak'
snak_ext = pythonDir + "snak_ext/"

# Setup the syntax files for specified text editor
if log.sys.argv[1] == "editor":
    # This will install snak syntax file to neovim
    if log.sys.argv[2] == "neovim": 
        try:

            shop.cp("editor/snak.vim", "/home/nathan/.config/nvim/syntax/")
        except FileNotFoundError:
            shop.mkdir("/home/nathan/.config/nvim/syntax")

    # Currently emacs is not supported
    elif log.sys.argv[2] == "emacs":
        log.Log(2, "Emacs Editor Support is Not Yet Implemented")

    # if editor is not in the list,
    # it will return an [Error]
    else:
        log.Log(3, f"Cannot find '{log.sys.argv[2]}' Editor")

# Install ql, ql source and scripts to localDir
elif log.sys.argv[1] == "install":
    # QL 
    shop.install(755, "snak.py", snak)
    
    # QL source directory
    shop.install(0, "snak-ext", snake_ext)

    # Scripts for the other functionalities of ql
    shop.install(755, "scripts/log.py", pythonDir+"log.py")
    shop.install(755, "scripts/shop.py", pythonDir+"shop.py")

# Remove folders/files if exists
elif log.sys.argv[1] == 'clean':
    try:
        # using the shop (Shell Operations) module
        shop.rem(snak)
        shop.rem(snake_ext+"*")
    except FileNotFoundError:
        pass
