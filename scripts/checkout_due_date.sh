#!/bin/bash

# Finds the last commit of a git repository thas was pushed before
# a given datetime. The datetime is typically the due date of the
# current assignment. Make sure to execute the script inside a folder
# that contains a git repository.
#
# usage: checkout_due_date.sh [datetime]
#   Params:
#   datetime    A valid datetime format is YYYY-MM-DDThh:mm. See git
#               log for more information on valid datetime formats.
#
# Error handling:
# - Exits with an error code when the 
#   %TASKNAME%_METRICS_JUNIT_POINTS_PER_TEST environment variable is not
#   set.
#
# This script is step 2 in the Deploy-to-Grading pipeline that is
# executed for the whole assignment.
#

usage() {
    # Print usage information
    cat <<EOM
usage: ./$(basename $0) [datetime]
  Checks out the last commit before the given datetime. This script
  needs to be run in a folder containing a git repository.

  Params:
  datetime    See git log documentation for valid datetime formats.
EOM
}

# Check if $1 is a valid datetime string
if ! date -d $1 2>: 1>:
then
    usage
    exit -1
fi

# Find first commit before the given datetime
COMMIT_ID=$(git log --before=$1 -n 1 | grep commit | cut -d' ' -f2)

if [ -z "$COMMIT_ID" ]
then
    echo "Error: No commit found before $1"
    usage
    exit -1
fi

# Checkout given commit id
git checkout -q $COMMIT_ID

# Check if checkout was successful
if [ ! $? -eq 0 ]
then
    echo "Error: Failed to checkout commit $COMMIT_ID"
    usage
    exit -1

echo "Successfully loaded commit with id $COMMIT_ID"

