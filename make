#!/bin/bash

if [[ $1 == "install" ]]; then
    echo "install -m755 mince $HOME/.local/bin/"
    install -m755 mince $HOME/.local/bin/
fi
