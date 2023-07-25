#!/bin/bash

# Wrapper for executing "gradle test". Make sure to execute the
# script inside a task folder that contains a gradle project.
# For correct functioning this script requires a correctly setup
# gradle task named "test" that saves the results to
# "build/results/junit/xml". A minimal example is:
#
# test {
#     useJUnit()
#     reports.junitXml.outputLocation = file("build/results/junit/xml")
# }
#
# usage: junit.sh
#
# This script is step 5 in the Deploy-to-Grading pipeline that is
# executed for every task that includes the junit metric.
#

# Execute junit tests using gradle
./gradlew test
exit 0
