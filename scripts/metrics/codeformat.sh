#!/bin/bash

# Wrapper for executing "gradle spotlessJavaCheck". Make sure to execute
# the script inside a task folder that contains a gradle project.
# The return value of the gradle execution is saved in a file
# "build/results/codeformat.yml".
#
# usage: codeformat.sh
#
# This script is step 5 in the Deploy-to-Grading pipeline that is
# executed for every task that includes the codeformat metric.
#

DIR=build/results

if [ ! -d "$DIR" ]
then
    mkdir -p "$DIR"
fi

./gradlew spotlessJavaCheck
echo "result: $?" > "$DIR/codeformat.yml"
