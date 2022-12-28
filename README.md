## Mince Programming Language


### Examples

```mince
defun test {
  print "Hello from mince"

  test_var
}

inv test
```


### FILES & DIRECTORIES
- [editor](./editor): for text editor support. 
- [examples](./examples): contains examples for you to test out

### INSTALLATION
##### For linux users
> for neo/vim users just copy the [filetype.vim](./editor/vim/filetype.vim)
> to '~/.config/nvim' for neovim or to '~/.vim' for vim.
> and the syntax file [mc.vim](./editor/vim/mc.vim) to '~/.config/nvim/syntax' or '~/.vim/syntax'

```bash
$ mkdir -p ~/.config/nvim/syntax # for neovim
$ mkdir -p ~/.vim/syntax # for vim

$ cp ./editor/vim/mc.vim ~/.config/nvim/syntax # for neovim
$ cp ./editor/vim/mc.vim ~/.vim/syntax # for vim

$ cp ./editor/vim/filetype.vim ~/.config/nvim # for neovim
$ cp ./editor/vim/filetype.vim ~/.vim # for vim

```

> to use mince you can compile it using:

```bash
$ sudo make clean install # it will install mince to /usr/local/bin
```

##### For Windows
> if your on Windows, it does not need any installation 
> just do the things below
> P.S use windows powershell to run these commands.

```bash
> git clone https://github.com/nathan-the-coder/mince  # assuming you have git installed 
> cd mince
```

> if you want to use just python then you can just do:

```bash
#to run the file you made just:
> .\mince.py # <your file>
# or
> python3 .\mince.py # <your file>
```

> you must have mingw-w64 installed with make to compile it
> if you want to compile it to machine code then just do:
```bash
# you must use windows powershell to be able to run these
make  
# to run it just 
.\mince # <your file>
```

> if you use neo/vim just do the steps above on how to apply the filetype 
> and syntax support, but change the '~/.config/nvim' to '%userprofile%\AppData\Local\nvim'
```bash
# you must use windows powershell to be able to run these
cp editor\vim\filetype.vim %userprofile%\AppData\Local\nvim

mkdir %userprofile%\AppData\Local\nvim\syntax

cp editor\vim\mc.vim %userprofile%\AppData\Local\nvim\syntax
```
> for vim change the '~/.vim' to '%userprofile%\AppData\Local\vim'
> P.S idk exactly the location of the user config of vim on Windows


### NEW
> I am still trying to figure out how to implement
> the incrementing and decrementing of a integer variable 

> remove some code that doesn't have functions and 
> change some keywords like from 'call' to 'inv',
> 'define' to 'defun', 'system' to 'exec'
> and remove 'println' which is replaced by 'print',
> also I added 'inc' and 'dec' keyword

> I did some refactoring of the code by making it simplier
> and much more readable

> I did made it to compile to machine code using Cython.

### Notes

> for function there is no parameters,
> simply because I can't code it, 
> I am only the one who code and implement 
> all of the code.

> this Language is not a toy language, 
> I will continue improving this and 
> with the capability to compile it 
> to machine code, It will be much more nicer.
