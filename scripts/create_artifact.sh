#!/bin/bash

# Copies the results folder from the indiviual tasks to the assignments
# result folder. The assignment and task configuration are also copied.
# Furthermore, this script creates a zip archive to distibute the results
# (e.g. as an artifact in the GitHub Action).
# Make sure that the $ASSIGNMENT_TASKS env variable contains a list of
# tasks seperated by whitespace.
#
# usage: create_artifact.sh
#
# This script is part of step 7 in the Deploy-to-Grading pipeline.
#

RESULTS_DIR=results
METRICS_DIR=metrics

# Copy task.yml and the results of every metric to the assignments
# result folder for every task
for TASK in $ASSIGNMENT_TASKS
do
    SRC_DIR=$TASK/build/results
    TARGET_DIR=$RESULTS_DIR/$TASK

    if [ ! -d "$TARGET_DIR/$METRICS_DIR/" ]
    then
        mkdir -p "$TARGET_DIR/$METRICS_DIR/"
    fi

    cp -r $SRC_DIR/* $TARGET_DIR/$METRICS_DIR/
    cp $TASK/task.yml $TARGET_DIR
done

# Copy assignment.yml
cp assignment.yml $RESULTS_DIR/

# Create zip archive from results folder
zip results.zip -r $RESULTS_DIR
