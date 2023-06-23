#!/bin/bash

usage() {
   cat <<EOM
usage: $(basename $0) [datetime]
EOM
    exit -1
}

if ! date -d $1 2>: 1>:
then
    usage
fi

COMMIT_ID=$(git log --before=$1 -n 1 | grep commit | cut -d' ' -f2)

if [ -z "$COMMIT_ID" ]
then
    echo "Error: No commit found before $1"
    exit -1
else
    git checkout $COMMIT_ID 2>: 1>:
fi

echo "Successfully loaded commit with id $COMMIT_ID"
