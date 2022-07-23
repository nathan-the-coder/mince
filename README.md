### Examples
```sn
! sample.sn

! define the method print
method << print [
    stdout << "Hello World"
]

! define the method main
method << main [
    stdout << "Hello?"
]

! call the method 'print' from the stack
stack << print
stack << main

stdout << "Demonstrating while loops"

```

Implementation
  Default: [Python](https://python.org)


> ### NEW
>  1. added [setup.py](./setup.py) to install additional modules and the python script itself.
>  2. added [log.py](./scripts/log.py) - used for pretty printing error's, warning's and to print msg.
>  3. added [shop.py](./scripts/shop.py) - used to run shell commands in python and used in [setup.py](./setup.py).

> ### REVAMPED
> 1. new name and syntax for this language

> ### REMOVED
> 1. removed server support, git integration, user input
