#!/bin/bash

# Wrapper for executing "gradle checkstyleMain" for stylechecking
# javadoc. Make sure to execute the script inside a task folder that
# contains a gradle project. For correct functioning this script
# requires a correctly setup checkstyle configuration that saves the
# results to "build/results/javadoc". A minimal example is:
#
# checkstyle {
#     toolVersion = "10.19.0"
#     configFile = file(".config/checkstyle/javadoc.xml")
#     reportsDir = file("build/results/javadoc")
# }
#
# tasks.withType(Checkstyle) {
#     reports {
#         xml.required = true
#         html.required = false
#     }
# }
#
# usage: javadoc.sh
#
# This script is step 5 in the Deploy-to-Grading pipeline that is
# executed for every task that includes the javadoc metric.
#

# Execute junit tests using gradle
./gradlew checkstyleMain
exit 0
