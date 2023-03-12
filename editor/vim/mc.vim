" Vim syntax file
" Language: mc Programming Language
" Maintainer: Nathaniel Ramos <nathanielramos726@gmail.com>
" Latest Revision: 31 July 2022

if exists("b:current_syntax")
  finish
endif

let s:cpo_save = &cpo
set cpo&vim

syn keyword mcTodo contained TODO FIXME XXX NOTE
syn match mcComment  "(\*).*$" contains=mcTodo,@Spell
syn match mcComment "\%^#!.*"

syn match mcNumber "\<\d\+\>"
" floating point number, with dot, optional exponent
syn match mcNumber  "\<\d\+\.\d*\%([eE][-+]\=\d\+\)\="
" floating point number, starting with a dot, optional exponent
syn match mcNumber  "\.\d\+\%([eE][-+]\=\d\+\)\=\>"
" floating point number, without dot, with exponent
syn match mcNumber  "\<\d\+[eE][-+]\=\d\+\>"

syn match  mcSpecial contained #\\[\\abfnrtv'"[\]]\|\\[[:digit:]]\{,3}#

syn region mcString matchgroup=mcStringDelimiter start=+'+ end=+'+ skip=+\\\\\|\\'+ contains=mcSpecial,@Spell
syn region mcString matchgroup=mcStringDelimiter start=+"+ end=+"+ skip=+\\\\\|\\"+ contains=mcSpecial,@Spell
syn region mcDesc start='"' end='"'

syn match mcFunction "\h\w*" display contained
syntax match mcFunc ":\@<=\k\+"

syn region mcDescBlock start="{" end="}" fold transparent contains=mcNumber, mcFunc, mcTodo, mcCond, mcRepeat, mcStatement, mcDesc, mcBuiltin, mcOperator, mcComment, mcString, mcConstant

syn keyword mcRepeat if else while
syn keyword mcFunction def print
syn keyword mcFunc print call exec read write panic min max let
syn keyword mcStatement break return
syn keyword mcConstant true false
syn keyword mcOperator or and


hi def link mcTodo              Todo
hi def link mcComment           Comment
hi def link mcStatement         Statement
hi def link mcBuiltin           Statement
hi def link mcFunc              Identifier
hi def link mcFunction          Function
hi def link mcCond              Conditional
hi def link mcCondElse          Conditional
hi def link mcConstant          Constant
hi def link mcString            String
hi def link mcStringDelimiter   mcString
hi def link mcDesc              Define
hi def link mcNumber            Number
hi def link mcRepeat            Repeat
hi def link mcOperator          Operator


let b:current_syntax = "mc"

let &cpo = s:cpo_save
unlet s:cpo_save
" vim: et ts=8 sw=2
