#!/bin/python3

# Evaluates the javadoc test results. It is required to execute javadoc.sh
# prior to the execution of this script. This script parses the test
# results saved in "build/results/javadoc" and converts them into the
# "results.yml" format defined in the 
# [documentation](https://github.com/Programmiermethoden/Deploy-to-Grading/blob/master/doc/design_document/d2g_procedure.md#format-der-result.yml).
# The output is printed to the console. Make sure to execute the script
# inside a task folder and that the task configuration defined in a
# task.yml file was loaded correctly using the load_yaml scripts.
#
# Points are calculated by deducting a number of points specified by the
# %TASKNAME%_METRICS_JAVADOC_DEDUCTION_PER_ERROR env variable from a maximum
# number of points specified by the %TASKNAME%_METRICS_JAVADOC_MAX_POINTS env
# variable. The minimum number of points is zero.
# This metric supports two different modes for calculating points. In the
# first mode, every error results in a point deduction. In the second mode,
# the errors are grouped by type and points are only deducted once per type.
# The mode can be switched by setting %TASKNAME%_METRICS_JAVADOC_GROUP_ERRORS
# env variable to true for the second mode.
#
# usage: javadoc_eval.py [taskname(optional)]
#   Params:
#   taskname    Name of the task used as prefix for the env variables.
#               If no taskname is given, "task" is used as the default
#               value.
#
# Error handling:
# - Exits with an error code when either of the 
#   %TASKNAME%_METRICS_JAVADOC_MAX_POINTS,
#   %TASKNAME%_METRICS_JAVADOC_GROUP_ERRORS
#   or %TASKNAME%_METRICS_JAVADOC_DEDUCTION_PER_ERROR environment variables
#   are not set.
#
# This script is part of step 6 in the Deploy-to-Grading pipeline that
# is executed for every task that includes the javadoc metric.
#

import os
import sys
import xml.etree.ElementTree as ET
import yaml

RESULT_FILE = "build/results/javadoc/main.xml"
MAX_POINTS_ENV_KEY = "%s_METRICS_JAVADOC_MAX_POINTS"
GROUP_ERRORS_ENV_KEY = "%s_METRICS_JAVADOC_GROUP_ERRORS"
DEDUCTION_PER_ERROR_ENV_KEY = "%s_METRICS_JAVADOC_DEDUCTION_PER_ERROR"

def _print_usage():
    print("usage: javadoc_eval.py [taskname(optional)]")
    print("       Make sure that javadoc.sh was executed prior to this")
    print("       script and that the task yaml was loaded successfully.")
    print("")
    print("       Params:")
    print("       taskname    Prefix of the task used for env variables.")

def _get_env_variable(taskname, key):
    # Combines taskname with key and returns its corresponding
    # environment variable. If the environment variable is not set,
    # it exits the program with an error.
    key = key % taskname.upper()

    if os.environ[key] is None:
        _print_usage()
        exit(-1)

    return os.environ[key]

def _load_xml_file():
    # Load xml result file.
    return ET.parse(RESULT_FILE)

def _get_relative_file_path(path):
    # Returns file path relative to the src directory.
    src_string = "src/"
    index = path.find(src_string)
    return path[index+len(src_string):]

def _get_error_type(class_path):
    # Extracts error name from the given class path.
    suffix = "Check"
    classname_start_index = class_path.rfind(".")
    return class_path[classname_start_index+1:-len(suffix)]

def _get_errors(data):
    # Extract errors from xml data. Returns a list of dicts with each
    # entry describing an error.
    errors = []
    for file in data.getroot():
        rel_file_path = _get_relative_file_path(file.attrib["name"])
        for error in file:
            errors.append({
                "source": "%s Ln %s, Col %s" % (rel_file_path,
                    error.attrib["line"], error.attrib["column"]),
                "message": error.attrib["message"],
                "type": _get_error_type(error.attrib["source"])
            })

    return errors

def _group_errors(errors):
    # Groups errors together based on error type.
    grouped_errors = {}

    for error in errors:
        if error["type"] in grouped_errors:
            grouped_errors[error["type"]]["source"] += "\n\t" + error["source"]
        else:
            grouped_errors[error["type"]] = {
                "source": error["source"],
                "message": error["message"],
                "type": error["type"]
            }

    return grouped_errors

def _convert_errors_to_mistakes(errors, max_points, deduction_per_error):
    # Converts errors into mistakes containing the descriptions and the
    # point deductions
    mistakes = []

    error_count = 0
    for error in errors:
        # Get actual error object when the errors are grouped.
        if isinstance(error, str):
            error = errors[error]

        mistakes.append({
            "deduction": deduction_per_error if error_count < max_points \
                else 0,
            "description": "%s: %s\n\t%s" % (error["type"], error["message"],
                error["source"])
        })
        error_count += deduction_per_error

    return mistakes

def _generate_final_results(mistakes, max_points, deduction_per_error):
    # Generates a results dictionary as defined in d2g_procedure.md in the
    # documentation and returns it.
    results = {
        "points": max(max_points - len(mistakes*deduction_per_error), 0),
        "max_points": max_points,
        "mistakes": mistakes
    }

    return results

def _print_results(results):
    # Prints results to the console as yaml.
    print(yaml.dump(results), end="")

def _main():
    taskname = "task"
    if len(sys.argv) == 2:
        taskname = sys.argv[1]

    # Load data from xml
    data = _load_xml_file()

    # Load environment variables
    max_points = int(_get_env_variable(taskname, MAX_POINTS_ENV_KEY))
    group_errors = True \
        if _get_env_variable(taskname, GROUP_ERRORS_ENV_KEY) == "true" else False
    deduction_per_error = int(_get_env_variable(taskname, 
        DEDUCTION_PER_ERROR_ENV_KEY))

    # Parse errors and group them if neccessary
    errors = _get_errors(data)
    if group_errors:
        errors = _group_errors(errors)

    # Create final yaml data
    mistakes = _convert_errors_to_mistakes(errors, max_points,
        deduction_per_error)
    results = _generate_final_results(mistakes, max_points,
        deduction_per_error)
    _print_results(results)

if __name__ == "__main__":
    _main()
