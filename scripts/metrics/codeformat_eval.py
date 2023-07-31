#!/bin/python3

# Evaluates the codeformat results. It is required to execute codeformat.sh
# prior to the execution of this script. This script parses the results
# saved in "build/results/codeformat.yml" and converts them into the "results.yml"
# format defined in the 
# [documentation](https://github.com/Programmiermethoden/Deploy-to-Grading/blob/master/doc/design_document/d2g_procedure.md#format-der-result.yml).
# The output is printed to the console. Make sure to execute the script
# inside a task folder and that the task configuration defined in a
# task.yml file was loaded correctly using the load_yaml scripts.
#
# usage: codeformat_eval.py [taskname(optional)]
#   Params:
#   taskname    Name of the task used as prefix for the env variables.
#               If no taskname is given, "task" is used as the default
#               value.
#
# Error handling:
# - Exits with an error code when the 
#   %TASKNAME%_METRICS_CODEFORMAT_POINTS environment variable is not
#   set or the results file was not found or could not be parsed.
#
# This script is part of step 6 in the Deploy-to-Grading pipeline that
# is executed for every task that includes the codeformat metric.
#

import os
import sys
import yaml

RESULTS_DIR = "build/results/"
RESULT_FILE = "codeformat.yml"

def _print_usage():
    print("usage: codeformat_eval.py [taskname(optional)]")
    print("       Make sure that codeformat.sh was executed prior to this")
    print("       script and that the task yaml was loaded correctly.")
    print("")
    print("       Params:")
    print("       taskname    Prefix of the task used for env variables.")

def _load_generated_results():
    # Loads the file build/results/codeformat.yml that contains the results
    # of the compilation and return them.
    try:
        with open(RESULTS_DIR+RESULT_FILE, "r") as file:
            try:
                return yaml.safe_load(file)
            except:
                print("Invalid yaml file")
                _print_usage()
                exit(-1)
    except FileNotFoundError as err:
        print("File %s not found" % RESULTS_DIR+RESULT_FILE)
        _print_usage()
        exit(-1)

def _generate_final_results(data, taskname):
    # Generates a results dictionary as defined in d2g_procedure.md in the
    # documentation and returns it. Requires the %TASKNAME%_METRICS_CODEFORMAT_POINTS
    # environment variable to be set.
    points = int(os.environ["%s_METRICS_CODEFORMAT_POINTS" % taskname.upper()])
    results = {
        "points": points if data["result"] == 0 else 0,
        "max_points": points
    }

    if data["result"] != 0:
        results["mistakes"] = [
            {
                "deduction": points,
                "description": "The code is not formatted correctly. \
Please format your code using spotless."
            }
        ]

    return results

def _print_results(results):
    # Prints results to the console as yaml.
    print(yaml.dump(results), end="")

def _main():
    taskname = "task"
    if len(sys.argv) == 2:
        taskname = sys.argv[1]

    data = _load_generated_results()
    results = _generate_final_results(data, taskname)
    _print_results(results)    

if __name__ == "__main__":
    _main()