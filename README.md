## Mince Programming Language  


### Examples
Here is a example of a mince script
```mc
# ./mince.py -e examples/sample.mc

# define the function print
define print {
  println! "Hello World"
}

# define the main function
define main {
  print! "Hello?\n"
  print! 1 + 1
  goto print
}

# call the main function
goto main
```


##### FILES & DIRECTORIES
1. the directory [editor](./editor) is where the editor's syntax files located.
2. the directory [examples](./examples) is where examples are stored.
3. the directory [mcs](./mcs) or I call it 'mince extensions' is soon contains extensions for mince.
4. the file [mince.py](./mince.py) is mince itself.
5. the directory [sedit](./sedit) is where my custom terminal text editor is located.


### NEW
1. added [log.py](./scripts/log.py) - used for pretty printing error's, warning's and to print msg.
2. added [shop.py](./scripts/shop.py) - used to run shell commands in python and used in [setup.py](./setup.py).
3. added [sedit](./sedit) - the editor i've made specifically for my language but only C files are syntax highlighted.

### REVAMPED
1. new name and syntax for this language. (2 times revamped)

### REMOVED
1. removed server support, git integration, user input.

## Notes
1. the setup.py is only usable on linux platform.
2. The 'print!' and 'println!' function is like rust's print functions.
3. Currently I wasn't able to implement function parameters because its hard to code :).
