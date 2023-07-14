#!/bin/python3

import os
import sys
import yaml

RESULTS_DIR = "build/results/"
RESULT_FILE = "compile.yml"

def _print_usage():
    print("usage: compile_eval.py [taskname(optional)]")
    print("       Make sure that compile.sh was executed prior to this")
    print("       script and that the task yaml was loaded correctly.")
    print("")
    print("       Params:")
    print("       taskname    Prefix of the task used for env variables.")
    exit(-1)

def _load_generated_results():
    # Loads the file build/results/compile.yml that contains the results
    # of the compilation and return them.
    try:
        with open(RESULTS_DIR+RESULT_FILE, "r") as file:
            try:
                return yaml.safe_load(file)
            except:
                print("Invalid yaml file")
                _print_usage()
    except FileNotFoundError as err:
        print("File %s not found" % RESULTS_DIR+RESULT_FILE)
        _print_usage()

def _generate_final_results(data, taskname):
    # Generates a results dictionary as defined in d2g_procedure.md in the
    # documentation and returns it. Requires the *TASKNAME*_METRICS_COMPILE_POINTS
    # environment variable to be set.
    points = int(os.environ["%s_METRICS_COMPILE_POINTS" % taskname.upper()])
    results = {
        "points": points if data["result"] == 0 else 0,
        "max_points": points
    }

    if data["result"] != 0:
        results["mistakes"] = [
            {
                "deduction": points,
                "description": "Compiltion failed."
            }
        ]

    return results

def _print_results(results):
    # Prints results to the console as yaml.
    print(yaml.dump(results), end="")

def _main():
    taskname = "task"
    if sys.argv == 2:
        taskname = sys.argv[1]

    data = _load_generated_results()
    results = _generate_final_results(data, taskname)
    _print_results(results)    

if __name__ == "__main__":
    _main()
