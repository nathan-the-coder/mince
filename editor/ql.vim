" Vim syntax file 
" Language Ql Programming Language
" Maintainer: Nathaniel Ramos
" Latest Revision: 22 May 2022


if exists("b:current_syntax")
  finish
endif

syn keyword qlTodo contained TODO FIXME XXX NOTE
syn match qlComment "*.*$" contains=qlTodo

syn match qlNumber '\d\+' contained display
syn match qlNumber '[-+]\d\+' contained display

syn match qlNumber '\d\+\.\d*' contained display
syn match qlNumber '[-+]\d\+\.\d*' contained display

syn match qlNumber '[-+]\=\d[[:digit:]]*[eE][\-+]\=\d\+' contained display
syn match qlNumber '\d[[:digit:]]*[eE]][\-+]\=\d\+' contained display

syn region qlString start='"' end='"' contained
syn region qlDesc start='"' end='"'

syn match qlHip '\d\{1,6}' nextgroup=qlString
syn match qlFunction    "\h\w*" display contained

syn match qlDecorator     "@" display contained
syn match qlDecoratorName "@\s*\h\%(\w\|\.\)*" display contains=qlDecorator



syn region qlDescBlock start="%" end="%" fold transparent contains=qlNumber, qlFunction, qlConditional, qlRepeat, qlStatement, qlBuiltin, qlOperator, qlComment 

" Keywords
syn keyword qlFunction DEFINE RUN OPEN INIT INPUT
syn keyword qlConditional IF ELSE 
syn keyword qlRepeat  WHILE
syn keyword qlStatement PRINT SERVE GIT CLONE 
syn keyword qlBuiltin BREAK EXIT 
syn keyword qlOperator OR AND TRUE FALSE 


let b:current_syntax = "ql"

hi def link qlTodo           Todo
hi def link qlComment        Comment 
hi def link qlStatement      Statement
hi def link qlFunction       Function
hi def link qlDecoratorName  Function
hi def link qlConditional    Conditional
hi def link qlString         String
hi def link qlDesc           Define 
hi def link qlNumber         Constant
hi def link qlRepeat         Repeat
hi def link qlOperator       Operator
