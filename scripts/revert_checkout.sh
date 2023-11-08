#!/bin/bash

# Reverts back the changes made by the checkout_due_date.sh script.
# Reads the previously checked out branch saved in 
# ./.d2g_previvous_checkout.txt and checks it out again.
#
# usage: revert_checkout.sh
#
# Error handling:
# - Does not handle errors.
#
# This script reverts step 2 of the Deploy-to-Grading pipeline.
#

FILE="./.d2g_previvous_checkout.txt"

if [ -e $FILE ]
then
    BRANCH=$(cat $FILE)
    git checkout $BRANCH
    rm $FILE
fi
