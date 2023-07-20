#!/bin/bash

# Wrapper for executing "gradle compileJava". Make sure to execute
# the script inside a task folder that contains a gradle project.
# The return value of the gradle execution is saved in a file
# "build/results/compile.yml".
#
# usage: compile.sh
#
# This script is step 5 in the Deploy-to-Grading pipeline that is
# executed for every task that includes the compile metric.
#

DIR=build/results

usage() {
    # Print usage information
    cat <<EOM
usage: ./$(basename $0)
  Runs gradle to compile the java code and saves the results.
EOM
}

if [ ! -d "$DIR" ]
then
    mkdir -p "$DIR"
fi

./gradlew compileJava
echo "result: $?" > "$DIR/compile.yml"

