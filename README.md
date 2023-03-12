# Mince Programming Language
A language that has C-like syntax, written in Python, compiled using Cython

#### IMPORTANT:
- To compile mince to binary using cython:
1. run `make install-cython` to compile mince on linux
2. or run `make compile-cython` to only compile mince if your on windows

- To compile mince to binary using nuitka:
1. run `make install-nuitka` to compile and install mince on linux
2. or run `make compile-nuitka` to only compile mince if your on windows

### NEW:
-  Mince is now standalone and modular
-  refer to [run.py](./run.py) to know how to make it modular

#### EXAMPLE:
  A simple Hello world program showcasing the 
  syntax of mince.

```mince
(*) this is a comment
def main {
  print "Hello from mince"
}
```

#### FILES & DIRECTORIES:
 files to enable editor support is in [editor](./editor)
 examples can be found at [examples](./examples)

#### INSTALLATION:
- if your using python 3.10 cp [Makefile.py310][./Makefile.py310] to Makefile and run the specified commands below
- use the command `make install-nuitka` to compile mince to binary using nuitka
- or use `make install-cython` to compile mince to binary using cython

##### References:
  [Cython]()
  [Python](https://python.org)

