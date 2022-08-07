# define the main function
define hello { 
    println! "This is the parent function"
    define nested {
        println! "This is a child function"
    
    call nested
}

call hello
