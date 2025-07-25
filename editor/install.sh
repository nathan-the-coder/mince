#!/bin/bash

NVIM_CFG=~/.config/nvim
case "$1" in
  "nvim")
    SYNTAX_DIR=$NVIM_CFG/syntax
    FTDETECT_DIR=$NVIM_CFG/ftdetect

    # Create the syntax and ftdetect dir inside of neovim config folder
    mkdir -p $SYNTAX_DIR $FTDETECT_DIR

    # Install neovim specific files for syntax and filetype detect file.
    install ./vim/filetype.vim $FTDETECT_DIR/mince.vim
    install ./vim/mince.vim $SYNTAX_DIR/mince.vim
    ;;
  *)
    printf "\e[0;33m[ERROR]: \e[0m Sorry, '$1' isn't supported yet."
    ;;
esac

