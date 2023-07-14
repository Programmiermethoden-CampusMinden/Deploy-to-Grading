#!/bin/bash

usage() {
    # Print usage information
    cat <<EOM
usage: ./$(basename $0) [datetime]
  Checks out the last commit before the given. This script needs to be
  run in a folder containing a git repository.

  Params:
  datetime    See git log documentation for valid datetime formats.
EOM
    exit -1
}

# Check if $1 is a valid datetime string
if ! date -d $1 2>: 1>:
then
    usage
fi

# Find first commit before the given datetime
COMMIT_ID=$(git log --before=$1 -n 1 | grep commit | cut -d' ' -f2)

if [ -z "$COMMIT_ID" ]
then
    echo "Error: No commit found before $1"
    usage
fi

# Checkout given commit id
git checkout -q $COMMIT_ID

# Check if checkout was successful
if [ ! $? -eq 0 ]
then
    echo "Error: Failed to checkout commit $COMMIT_ID"
    usage
else
    echo "Successfully loaded commit with id $COMMIT_ID"
fi

