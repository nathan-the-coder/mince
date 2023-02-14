" Vim syntax file
" Language: Mince Programming Language
" Maintainer: Nathaniel Ramos <nathanielramos726@gmail.com>
" Latest Revision: 31 July 2022

if exists("b:current_syntax")
  finish
endif

let s:cpo_save = &cpo
set cpo&vim

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
syn keyword minceFunction def end then
syn keyword minceFunc print println inv exec read write panic min max inc dec
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
hi def link minceCondElse          Conditional
hi def link minceConstant          Constant
hi def link minceString            String
hi def link minceStringDelimiter   minceString
hi def link minceDesc              Define
hi def link minceNumber            Number
hi def link minceRepeat            Repeat
hi def link minceOperator          Operator


let b:current_syntax = "mince"

let &cpo = s:cpo_save
unlet s:cpo_save
" vim: et ts=8 sw=2
