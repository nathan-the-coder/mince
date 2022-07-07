#!/usr/bin/env python3
import log
import shop

localDir = "/home/nathan/.local/"
pythonDir = localDir + "lib/python3.10/site-packages/"
ql = localDir + 'bin/ql'
qls = pythonDir + "qls"

if log.sys.argv[1] == "editor":
    if log.sys.argv[2] == "neovim": 
        try:
            shop.cp("editor/ql.vim", "/home/nathan/.config/nvim/syntax/")
        except FileNotFoundError:
            shop.mkdir("/home/nathan/.config/nvim/syntax")

    elif log.sys.argv[2] == "emacs":
        log.Log(2, "Emacs Editor Support is Not Yet Implemented")

    else:
        log.Log(3, f"Cannot find '{log.sys.argv[2]}' Editor")
elif log.sys.argv[1] == "install":
    shop.install(755, "ql.py", ql)
    shop.install(755, "qls", qls)
    shop.install(755, "scripts/log.py", pythonDir+"log.py")
    shop.install(755, "scripts/shop.py", pythonDir+"shop.py")
elif log.sys.argv[1] == 'clean':
    try:
        shop.rem(ql)
        shop.rem(qls+"/*")
    except FileNotFoundError:
        pass
