
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

every method defined the methods stack will increment
and when dumped it will show the number of methods defined,
```snak
dump >> methods # < 'methods' is one of the variables that can be accessed using 'dump'
# ^ 'dump' will print how many methods is defined,
> 1
```

I also want to add that you can call a methods in the stack
to run the method like so:.

```snak 
stack >> print # < 'print' is the method that we define above
# ^ is the stack containing methods that is defined
```
