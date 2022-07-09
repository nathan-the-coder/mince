#!/usr/bin/env python3

# Import the scripts to be used inside the setup.py
from scripts import log, shop

# Variables to store directories used by the conditionals
localDir = "/home/nathan/.local/"
pythonDir = localDir + "lib/python3.10/site-packages/"
ql = localDir + 'bin/ql'
qls = pythonDir + "qls/"

# Setup the syntax files for specified text editor
if log.sys.argv[1] == "editor":
    # This will install ql syntax file to neovim
    if log.sys.argv[2] == "neovim": 
        try:

            shop.cp("editor/ql.vim", "/home/nathan/.config/nvim/syntax/")
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
    shop.install(755, "ql.py", ql)
    
    # QL source directory
    shop.install(0, "qls", qls)

    # Scripts for the other functionalities of ql
    shop.install(755, "scripts/log.py", pythonDir+"log.py")
    shop.install(755, "scripts/shop.py", pythonDir+"shop.py")
    shop.install(755, "scripts/git.py", pythonDir+"git.py")

# Remove folders/files if exists
elif log.sys.argv[1] == 'clean':
    try:
        # using the shop (Shell Operations) module
        shop.rem(ql)
        shop.rem(qls+"*")
    except FileNotFoundError:
        pass
