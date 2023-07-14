#!/bin/bash

usage() {
    # Print usage information
    cat <<EOM
usage: ./$(basename $0) [yaml]
  Exports configuration in 'yaml' to environment variables.

  Params:
  yaml    Path to file containing configuration data in yaml format
EOM
    
    # We don't want to exit the shell when the script
    # is started using source
    if [ ! $(dirname -- "$0") = "." ]
    then
        exit -1
    fi
}

# Run python script to load yaml
output=$($D2G_PATH/scripts/load_yaml.py "$@")

if [ ! $? -eq 0 ]
then
    echo $output
    usage
fi

# Execute code generated by the python script
eval $output