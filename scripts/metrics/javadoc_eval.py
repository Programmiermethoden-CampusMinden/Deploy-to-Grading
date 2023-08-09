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

import metric_utils

RESULT_FILE = "build/results/javadoc/main.xml"

MAX_POINTS_ENV_KEY = "%s_METRICS_JAVADOC_MAX_POINTS"
GROUP_ERRORS_ENV_KEY = "%s_METRICS_JAVADOC_GROUP_ERRORS"
DEDUCTION_PER_ERROR_ENV_KEY = "%s_METRICS_JAVADOC_DEDUCTION_PER_ERROR"

USAGE = """usage: javadoc_eval.py [taskname(optional)]
       Make sure that javadoc.sh was executed prior to this
       script and that the task yaml was loaded successfully.

       Params:
       taskname    Prefix of the task used for env variables.
"""

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

        mistakes.append(metric_utils.create_mistake(
            deduction_per_error if error_count < max_points else 0,
            "%s: %s\n\t%s" % (error["type"], error["message"], error["source"])
        ))
        error_count += deduction_per_error

    return mistakes

def _main():
    taskname = metric_utils.get_taskname()

    # Load data from xml
    data = metric_utils.load_xml_file(RESULT_FILE, USAGE)

    # Load environment variables
    max_points = int(metric_utils.get_env_variable(
        MAX_POINTS_ENV_KEY, taskname, USAGE))
    group_errors = True if metric_utils.get_env_variable(
        GROUP_ERRORS_ENV_KEY, taskname, USAGE) == "true" else False
    deduction_per_error = int(metric_utils.get_env_variable(
        DEDUCTION_PER_ERROR_ENV_KEY, taskname, USAGE))

    # Parse errors and group them if neccessary
    errors = _get_errors(data)
    if group_errors:
        errors = _group_errors(errors)

    # Create final yaml data
    mistakes = _convert_errors_to_mistakes(errors, max_points,
        deduction_per_error)
    results = metric_utils.generate_final_results_deduction_per_error(
        mistakes, max_points, deduction_per_error)
    metric_utils.print_results(results)

if __name__ == "__main__":
    _main()
