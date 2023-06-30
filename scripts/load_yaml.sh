#!/bin/bash

if [ $(dirname -- "$0") = "." ]
then
    output=$(./scripts/load_yaml.py "$@")
else
    output=$($(dirname -- "$0")/load_yaml.py "$@")
fi

if [ ! $? -eq 0 ]
then
    echo $output
    
    # We don't want to exit the shell when the script
    # is started using source
    if [ ! $(dirname -- "$0") = "." ]
    then
        exit $?
    fi
fi

eval $output
