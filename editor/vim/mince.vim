" Vim syntax file
" Language: Mince Programming Language
" Maintainer: Nathaniel Ramos <nathanielramos726@gmail.com>
" Latest Revision: 31 July 2022

if exists("b:current_syntax")
  finish
endif
syn keyword minceTodo contained TODO FIXME XXX NOTE
syn match minceComment '#.*$' contains=minceTodo

syn match minceNumber '\d\+' contained display
syn match minceNumber '[-+]\d\+' contained display

syn match mcNumber '[-+]\=\d[[:digit:]]*[eE][\-+]\=\d\+' contained display
syn match mcNumber '\d[[:digit:]]*[eE]][\-+]\=\d\+' contained display

syn region mcString start='"' end='"' contained
syn region minceDesc start='"' end='"'

syn match minceFunction "\h\w*" display contained

syn region minceDescBlock start="{" end="}" fold transparent contains=minceNumber, minceTodo, minceConditional, minceRepeat, minceStatement, minceDesc, minceBuiltin, minceOperator, minceComment, minceString

syn keyword minceFunction define 
syn keyword minceConditional if else
syn keyword minceRepeat while
syn keyword minceStatement print println goto system read write
syn keyword minceBuiltin break exit true false
syn keyword minceOperator or and 

let b:current_syntax = "mince"

hi def link minceTodo              Todo
hi def link minceComment           Comment
hi def link minceStatement         Statement
hi def link minceFunction          Function
hi def link minceConditional       Conditional
hi def link minceString            String
hi def link minceDesc              Define
hi def link minceNumber            Constant
hi def link minceRepeat            Repeat
hi def link minceOperator          Operator

