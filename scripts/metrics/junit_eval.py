#!/bin/python3

import os
import sys
import xml.etree.ElementTree as ET
import yaml

RESULT_PATH = "build/results/junit/xml"
POINTS_PER_TEST_ENV_KEY = "%s_METRICS_JUNIT_POINTS_PER_TEST"

def _print_usage():
    print("usage: junit_eval.py [taskname(optional)]")
    print("       Make sure that junit.sh was executed prior to this")
    print("       script and that the task yaml was loaded successfully.")
    print("")
    print("       Params:")
    print("       taskname    Prefix of the task used for env variables.")
    exit(-1)

def _get_points_per_test_env_variable(taskname):
    # Gets the points per test from the environment variables.
    # If the environment variable is not set, it returns a
    # default value of 1
    key = POINTS_PER_TEST_ENV_KEY % taskname.upper()
    if os.environ[key] is not None:
        return int(os.environ[key])
    _print_usage()

def _load_xml_files():
    # Load all xml files in RESULT_PATH.
    data = []
    for _, _, files in os.walk(RESULT_PATH):
        for file in files:
            data.append(ET.parse(os.path.join(RESULT_PATH, file)))
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

def _generate_final_results(test_count, mistakes, points_per_test):
    # Generates a results dictionary as defined in d2g_procedure.md in the
    # documentation an returns it.
    results = {
        "points": (test_count[0]-test_count[1]) * points_per_test,
        "max_points": test_count[0] * points_per_test,
        "mistakes": mistakes
    }

    return results

def _print_results(results):
    # Prints results to the console as yaml.
    print(yaml.dump(results), end="")

def _main():
    taskname = "task"
    if sys.argv == 2:
        taskname = sys.argv[1]

    data = _load_xml_files()
    points_per_test = _get_points_per_test_env_variable(taskname)
    test_count = _count_tests(data)
    mistakes = _summarize_mistakes(data, points_per_test)

    results = _generate_final_results(test_count, mistakes, points_per_test)
    _print_results(results)

if __name__ == "__main__":
    _main()
