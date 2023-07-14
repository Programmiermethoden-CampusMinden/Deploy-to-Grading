#!/bin/bash

usage() {
    # Print usage information
    cat <<EOM
usage: ./$(basename $0)
  Wrapper for executing gradle test.
EOM
}

./gradlew test
