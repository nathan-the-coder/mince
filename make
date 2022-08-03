#!/bin/bash

if [[ $1 == "install" ]]; then
    echo "cp ./mince $HOME/.local/bin/mince"
    cp ./mince $HOME/.local/bin/mince
fi
