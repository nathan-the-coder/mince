# On Linux

### Neo(Vim)
Neovim:
- copy the [filetype.vim](./editor/vim/filetype.vim) to either [neovim runtime](/usr/share/nvim/runtime/) or [neovim config folder](~/.config/nvim) and 
- copy the [mc.vim](./editor/vim/mc.vim) file to [neovim syntax folder](/usr/share/neovim/runtime/syntax/) or [vim '~/.vim/syntax'

Vim:
- copy the [filetype.vim](./editor/vim/filetype.vim) to either [vim runtime in root](/usr/share/vim90/) or [vim config folder](~/.vim)
- copy the [mc.vim](./editor/vim/mc.vim) file to either [vim syntax folder in root](/usr/share/vim90/syntax/) or [vim syntax folder in config dir](~/.vim/syntax)

#### Use `make` to compile the source code and `sudo make install` to install it to /usr/local/bin.

# On Windows
- To install/use the interpreter in Windows, you need WSL or:
- Install a Linux distro
- My recommendations are [Debian](https://debian.org) or [Arch Linux](https://archlinux.org)
