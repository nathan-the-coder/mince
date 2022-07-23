" Vim syntax file 
" Language: Snak Programming Language
" Maintainer: Nathaniel Ramos
" Latest Revision: 22 May 2022


if exists("b:current_syntax")
  finish
endif

syn keyword snakTodo contained TODO FIXME XXX NOTE
syn match snakComment "#.*$" contains=qlTodo

syn match snakNumber '\d\+' contained display
syn match snakNumber '[-+]\d\+' contained display

syn match snakNumber '\d\+\.\d*' contained display
syn match snakNumber '[-+]\d\+\.\d*' contained display

syn match snakNumber '[-+]\=\d[[:digit:]]*[eE][\-+]\=\d\+' contained display
syn match snakNumber '\d[[:digit:]]*[eE]][\-+]\=\d\+' contained display

syn region snakString start='"' end='"' contained
syn region snakDesc start='"' end='"'

syn match snakHip '\d\{1,6}' nextgroup=qlString
syn match snakFunction    "\h\w*" display contained

syn match snakDecorator     "@" display contained
syn match snakDecoratorName "@\s*\h\%(\w\|\.\)*" display contains=snakDecorator



syn region snakDescBlock start="[" end="]" fold transparent contains=snakNumber, snakFunction, snakConditional, snakRepeat, snakStatement,  snakBuiltin, snakOperator, snakComment 

" Keywords
syn keyword snakFunction << method stack dump 
syn keyword snakConditional if else
syn keyword snakRepeat while
syn keyword snakStatement stdout  
syn keyword snakBuiltin break exit 
syn keyword snakOperator or and True False 


let b:current_syntax = "snak"

hi def link snakTodo           Todo
hi def link snakComment        Comment 
hi def link snakStatement      Statement
hi def link snakFunction       Function
hi def link snakDecoratorName  Function
hi def link snakConditional    Conditional
hi def link snakString         String
hi def link snakDesc           Define 
hi def link snakNumber         Constant
hi def link snakRepeat         Repeat
hi def link snakOperator       Operator