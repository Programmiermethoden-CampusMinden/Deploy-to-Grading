#!/bin/bash

DIR=build/results

if [ ! -d "$DIR" ]
then
    mkdir -p "$DIR"
fi

./gradlew compileJava
echo "result: $?" > "$DIR/compile.yml"

