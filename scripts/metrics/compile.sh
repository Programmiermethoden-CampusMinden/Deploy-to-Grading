#!/bin/bash

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

