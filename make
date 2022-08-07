#!/bin/bash
make="make: ***"

if [[ $1 == "install" ]]; then
    echo "install -m755 mince $HOME/.local/bin/"
    install -m755 mince $HOME/.local/bin/
elif [[ $1 == "" ]]; then
    echo "$make No targets.  Stop." 
else
    echo "$make No rule to make target '$1'.  Stop."
    exit
fi
