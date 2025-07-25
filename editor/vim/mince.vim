" Syntax highlighting for Mince

syntax keyword minceKeyword let fnc if else while break return out fail exec
syntax keyword minceBuiltin min max clock

" Built-in functions
syntax keyword minceFunction print println panic

" Boolean and null-like
syntax keyword minceBoolean true false null

" Comments
syntax match minceComment "#.*$"

" Strings
syntax region minceString start=/"/ skip=/\\"/ end=/"/

" Numbers
syntax match minceNumber "\v\d+"

" Function calls (basic match)
syntax match minceCall "\<[a-zA-Z_][a-zA-Z0-9_]*\s*("

" Highlight groups
highlight link minceKeyword Keyword
highlight link minceBuiltin Function
highlight link minceFunction Function
highlight link minceBoolean Boolean
highlight link minceComment Comment
highlight link minceString String
highlight link minceNumber Number
highlight link minceCall Identifier

