" Vim syntax file
" Language: Mince Programming Language
" Maintainer: Nathaniel Ramos <nathanielramos726@gmail.com>
" Latest Revision: 31 July 2022

if exists("b:current_syntax")
  finish
endif

let s:cpo_save = &cpo
set cpo&vim

" else
syn keyword minceCondElse matchgroup=luaCond contained containedin=minceCondEnd else

" then ... end
syn region minceCondEnd contained transparent matchgroup=minceCond start="\<then\>" end="\<end\>" contains=TOP

" if ... then
syn region minceCondStart transparent matchgroup=minceCond start="\<if\>" end="\<then\>"me=e-4 contains=TOP nextgroup=luaCondEnd skipwhite skipempty

" do ... end
syn region minceBlock transparent matchgroup=minceStatement start="\<do\>" end="\<end\>" contains=TOP

" while ... do
syn region minceWhile transparent matchgroup=minceRepeat start="\<while\>" end="\<do\>"me=e-2 contains=TOP nextgroup=minceBlock skipwhite skipempty


syn keyword minceTodo contained TODO FIXME XXX NOTE
syn match minceComment  "#.*$" contains=minceTodo,@Spell
syn match minceComment "\%^#!.*"

syn match minceNumber "\<\d\+\>"
" floating point number, with dot, optional exponent
syn match minceNumber  "\<\d\+\.\d*\%([eE][-+]\=\d\+\)\="
" floating point number, starting with a dot, optional exponent
syn match minceNumber  "\.\d\+\%([eE][-+]\=\d\+\)\=\>"
" floating point number, without dot, with exponent
syn match minceNumber  "\<\d\+[eE][-+]\=\d\+\>"

syn match  minceSpecial contained #\\[\\abfnrtv'"[\]]\|\\[[:digit:]]\{,3}#

syn region minceString matchgroup=minceStringDelimiter start=+'+ end=+'+ skip=+\\\\\|\\'+ contains=minceSpecial,@Spell
syn region minceString matchgroup=minceStringDelimiter start=+"+ end=+"+ skip=+\\\\\|\\"+ contains=minceSpecial,@Spell
syn region minceDesc start='"' end='"'

syn match minceFunction "\h\w*" display contained
syntax match luaFunc ":\@<=\k\+"

syn region minceDescBlock start="{" end="}" fold transparent contains=minceNumber, minceFunc, minceTodo, minceCond, minceRepeat, minceStatement, minceDesc, minceBuiltin, minceOperator, minceComment, minceString, minceConstant

syn keyword minceRepeat while
syn keyword minceFunction defun
syn keyword minceFunc print inv exec read write panic
syn keyword minceStatement break return
syn keyword minceConstant true false
syn keyword minceOperator or and


hi def link minceTodo              Todo
hi def link minceComment           Comment
hi def link minceStatement         Statement
hi def link minceBuiltin           Statement
hi def link minceFunc              Identifier
hi def link minceFunction          Function
hi def link minceCond              Conditional
hi def link minceConstant          Constant
hi def link minceString            String
hi def link minceStringDelimiter   minceString
hi def link minceDesc              Define
hi def link minceNumber            Number
hi def link minceRepeat            Repeat
hi def link minceOperator          Operator


let b:current_syntax = "mc"

let &cpo = s:cpo_save
unlet s:cpo_save
" vim: et ts=8 sw=2
