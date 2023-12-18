// define the main function
define hello { 
    echo "This is the parent function\n"
    define nested {
        echo "This is a child function\n"
    }
    
    call nested
}

call hello
