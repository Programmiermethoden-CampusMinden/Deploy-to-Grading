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
import sys

RESULT_PATH = "build/results/junit/xml"

POINTS_PER_TEST_ENV_KEY = "%s_METRICS_JUNIT_POINTS_PER_TEST"

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

def _count_tests(data):
    # Summarizes the overall number of tests and the number
    # of failed tests. Returns a tuple (tests, failed_tests).
    tests = 0
    failed_tests = 0

    for testsuite in data:
        root = testsuite.getroot()
        # Note: Skipped tests are not counted towards either
        #       of those values.
        tests = int(root.attrib["tests"])
        failed_tests = int(root.attrib["failures"]) \
                     + int(root.attrib["errors"])
    
    return (tests, failed_tests)

def _summarize_mistakes(data, points_per_test):
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
                    "deduction": points_per_test,
                    "description": description
                })

    return mistakes

def _main():
    taskname = "task"
    if len(sys.argv) == 2:
        taskname = sys.argv[1]

    data = _load_xml_files()
    points_per_test = int(metric_utils.get_env_variable(
        POINTS_PER_TEST_ENV_KEY, taskname, USAGE))
    test_count = _count_tests(data)
    mistakes = _summarize_mistakes(data, points_per_test)

    results = metric_utils.generate_final_results_points_per_test(
        mistakes, test_count, points_per_test)
    metric_utils.print_results(results)

if __name__ == "__main__":
    _main()
