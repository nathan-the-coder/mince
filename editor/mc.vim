" Vim syntax file
" Language: Mince Programming Language
" Maintainer: Nathaniel Ramos <nathanielramos726@gmail.com>
" Latest Revision: 31 July 2022

if exists("b:current_syntax"
  finish
endif
syn keyword mcTodo contained TODO FIXME XXX NOTE
syn match mcComment #.*$ contains=mcTodo

syn match mcNumber '\d\+' contained display
syn match mcNumber '[-+]\d\+' contained display

syn match mcNumber '[-+]\=\d[[:digit:]]*[eE][\-+]\=\d\+' contained display
syn match mcNumber '\d[[:digit:]]*[eE]][\-+]\=\d\+' contained display

syn region mcString start='"'end='"' contained
syn region mcDesc start='"'end='"'

syn match mcHip '\d\{1.6}' nextgroup=mcString
syn match mcFunction "\h\w*" display contained

syn region mcDescBlock start="{" end="}" fold transparent contains=mcNumber, mcFunction, mcTodo, mcConditional, mcRepeat, mcStatement, mcDesc, mcBuiltin, mcOperator, mcComment, mcString

" Keywords
syn keyword mcFunction define goto
syn keyword mcConditional if else
syn keyword mcRepeat while
syn keyword mcStatement print! println!
syn keyword mcBuiltin break exit
syn keyword mcOperator or and true false

" Set current syntax
let b:current_syntax = "mc"

" highlighting 
hi def link mcTodo              Todo
hi def link mcComment           Comment
hi def link mcStatement         Statement
hi def link mcFunction          Function
hi def link mcConditional       Conditional
hi def link mcString            String
hi def link mcDesc              Define
hi def link mcNumber            Constant
hi def link mcRepeat            Repeat
hi def link mcOperator          Operator

