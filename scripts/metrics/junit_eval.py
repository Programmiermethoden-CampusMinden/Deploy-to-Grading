#!/bin/python3

# Evaluates the junit test results. It is required to execute junit.sh
# prior to the execution of this script. This script parses the test
# results saved in "build/results/junit/xml" and converts them into the
# "results.yml" format defined in the 
# [documentation](https://github.com/Programmiermethoden/Deploy-to-Grading/blob/master/doc/design_document/d2g_procedure.md#format-der-result.yml).
# The output is printed to the console. Make sure to execute the script
# inside a task folder and that the task configuration defined in a
# task.yml file was loaded correctly using the load_yaml scripts.
#
# usage: junit_eval.py [taskname(optional)]
#   Params:
#   taskname    Name of the task used as prefix for the env variables.
#               If no taskname is given, "task" is used as the default
#               value.
#
# Error handling:
# - Exits with an error code when the 
#   %TASKNAME%_METRICS_JUNIT_POINTS_PER_TEST environment variable is not
#   set.
#
# This script is part of step 6 in the Deploy-to-Grading pipeline that
# is executed for every task that includes the junit metric.
#

import metric_utils
import os
import re

RESULT_PATH = "build/results/junit/xml"

DEFAULT_POINTS_ENV_KEY = "%s_METRICS_JUNIT_DEFAULT_POINTS"

USAGE = """usage: junit_eval.py [taskname(optional)]
       Make sure that junit.sh was executed prior to this
       script and that the task yaml was loaded successfully.

       Params:
       taskname    Prefix of the task used for env variables.
"""

def _load_xml_files():
    # Load all xml files in RESULT_PATH.
    data = []
    for _, _, files in os.walk(RESULT_PATH):
        for file in files:
            data.append(metric_utils.load_xml_file(
                os.path.join(RESULT_PATH, file), USAGE))
    return data

def _get_points_of_test(testname, default_points):
    # Determines the possible points of a test case based on its name.
    # It is possible to give tests a custom number of points by
    # appending "_%POINTS%p" to the name of the test where %POINTS%
    # is replaced with an integer value.
    match = re.search(r"_\d+[pP]$", testname)
    if match:
        return match.group(0)[1:-1]
    return default_points

def _get_points(data, default_points):
    points = 0
    max_points = 0

    for testsuite in data:
        root = testsuite.getroot()
        for testcase in root:
            if testcase.tag == "testcase":
                possible_points = _get_points_of_test(testcase.attrib["name"],
                                                      default_points)
                if len(testcase) == 0:
                    points += possible_points
                max_points += possible_points
    
    return (points, max_points)

def _summarize_mistakes(data, default_points):
    # Collect all failed test cases and create a summery containing
    # the deduction and a description of the error.
    mistakes = []
    for testsuite in data:
        root = testsuite.getroot()
        for testcase in root:
            if testcase.tag == "testcase" and len(testcase) > 0:
                description = "%s::%s: %s" % (root.attrib["name"], \
                    testcase.attrib["name"], testcase[0].attrib["message"])
                mistakes.append({
                    "deduction": _get_points_of_test(testcase.attrib["name"],
                                                     default_points),
                    "description": description
                })

    return mistakes

def _main():
    taskname = metric_utils.get_taskname()

    data = _load_xml_files()
    default_points = int(metric_utils.get_env_variable(
        DEFAULT_POINTS_ENV_KEY, taskname, USAGE))
    points, max_points = _get_points(data, default_points)
    mistakes = _summarize_mistakes(data, default_points)

    results = metric_utils._generate_final_results(
        mistakes, points, max_points)
    metric_utils.print_results(results)

if __name__ == "__main__":
    _main()
