#!/bin/bash

DIR=build/results

if [ ! -d "$DIR" ]
then
    mkdir -p "$DIR"
fi

gradle compileJava
echo "result: $?" > "$DIR/compile.yml"

