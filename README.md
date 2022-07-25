## Snak Programming Language  


### Examples
```sn
# ./snak.py -e sample.sn

# define the method print
method << print [
    stdout << "Hello World"
]

# define the method main
method << main [
    stdout << "Hello?"
]

# call the method 'print' from the stack
stack << print
stack << main

# watched how many methods defined
dump >> methods

```

### NEW
1. added [setup.py](./setup.py) to install additional modules and the python script itself.
2. added [log.py](./scripts/log.py) - used for pretty printing error's, warning's and to print msg.
3. added [shop.py](./scripts/shop.py) - used to run shell commands in python and used in [setup.py](./setup.py).
4. added [sedit](./sedit) - the editor i've made specifically for my language but there is no syntax highlighting yet.

### REVAMPED
1. new name and syntax for this language.

### REMOVED
1. removed server support, git integration, user input.

## Notes
1. If the snak.py not work on linux or macos, try dos2unix.
2. the setup.py is only usable on linux platform.
3. Snak is different from the esolang caled snak - differences are the syntax.
