## Mince Programming Language


### Examples

```c
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

```console
mkdir -p ~/.config/nvim/syntax # for neovim
mkdir -p ~/.vim/syntax # for vim

cp ./editor/vim/mc.vim ~/.config/nvim/syntax # for neovim
cp ./editor/vim/mc.vim ~/.vim/syntax # for vim

cp ./editor/vim/filetype.vim ~/.config/nvim # for neovim
cp ./editor/vim/filetype.vim ~/.vim # for vim

```

> if you want to use mince outside of its directory 
> you can install it using:

```console
./make install  # P.S not a make script
```
##### For Windows
> if your on Windows, it does not need any installation 
> just clone this repo and you dont need to run the [make](./make) file

```console
git clone https://github.com/nathan-the-coder/mince  # assuming you have git installed 
cd mince

# to run the file you made just:
.\mince <your file>
# or
python3 .\mince <your file>
```

> if you use neo/vim just do the steps above on how to apply the filetype 
> and syntax support, but change the '~/.config/nvim' to '%userprofile%\AppData\Local\nvim'
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

### Notes

> for function there is no parameters,
> simply because I can't code it, 
> I am only the one who code and implement 
> all of the code.

> this Language is not a toy language, 
> I will continue improving this and 
> maybe reimplement it in a different language 
> like 'C' or 'Rust' or 'Lua'
