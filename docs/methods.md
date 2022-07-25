
methods in Snak is like the function in any other languages

you can define a method using:
```snak
method << print [
    stdout << "Hello World"  
]

> 
```

and also stdout is the print method in snak.

but methods in snak cannot have a parameter.


I also want to add that you can call a methods in the stack
to run the method like so:.

```snak 
stack >> print # < 'print' is the method that we define above
# ^ is the stack containing methods that is defined
```
