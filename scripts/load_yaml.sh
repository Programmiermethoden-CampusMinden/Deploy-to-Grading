#!/bin/bash

output=$($D2G_PATH/scripts/load_yaml.py "$@")

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
