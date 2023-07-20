#!/bin/python3

# Collects and summarizes the results of all defined metrics for a given
# task. This script automatically executes all evaluation scripts for the
# metrics defined in the environment variable %TASKNAME%_METRICS. The 
# output is captured and merged into the format described in the
# [documentation](https://github.com/Programmiermethoden/Deploy-to-Grading/blob/master/doc/design_document/d2g_procedure.md#format-der-result.yml).
# and printed to the console. As metric evaluation scripts, both bash and
# python scripts are accepted. To create a new metric evaluation script,
# you must follow the rules mentioned in the [documentation](TODO).
# Make sure to execute the script inside a task folder and that the task
# configuration defined in a task.yml file was loaded correctly using the
# load_yaml scripts. Furthermore, the D2G_PATH environment variable must be
# set to the path containing the Deploy-to-Grading pipeline.
#
# usage: evaluate_task.py [taskname(optional)]
#   Params:
#   taskname    Name of the task used as prefix for the env variables and
#               inside the path to the final results.yml file. If no
#               taskname is given, "task" is used as the default value.
#
# Error handling:
# - Exits with an error code when the %TASKNAME%_METRICS environment
#   variable is not set or a metric specific script failed to execute
#   correctly.
#
# This script is the main script of step 6 in the Deploy-to-Grading pipeline
# that is executed for every task.
#

import os
import subprocess
import sys
import yaml

def _print_usage():
    print("usage: evaluate_task.py [taskname(optional)]")
    print("       Requires that environment variables *TASKNAME*_METRICS")
    print("       and D2G_PATH are set.")
    print("")
    print("       Params:")
    print("       taskname    Prefix of the task used for env variables.")

def _get_metrics_list(taskname):
    # Load a list of all metrics used in this task. The list is loaded
    # from the environment variable *TASKNAME*_METRICS.
    metrics_string = os.environ["%s_METRICS" % taskname.upper()]

    if not metrics_string or metrics_string == "":
        _print_usage()
        exit(-1)

    return metrics_string.split(" ")

def _get_script_path(metric):
    # Search for an evaluation script for the given metrics.
    # Looks for scripts written in bash or python
    base_path = os.path.join(os.environ["D2G_PATH"],
        "scripts/metrics/%s_eval" % metric)
    if os.path.exists(base_path + ".sh"):
        return base_path + ".sh"
    elif os.path.exists(base_path + ".py"):
        return base_path + ".py"
    else:
        return None

def _evaluate_metric(metric, taskname):
    # Execute the evaluation script of the given metric and return its
    # output as yaml.
    script = _get_script_path(metric)
    print(script)
    if script is None:
        print("No script found to evaluate metric %s" % metric)
        _print_usage()
        exit(-1)

    proc = subprocess.run([script, taskname], capture_output=True)
    if proc.returncode != 0:
        print("Failed to evaluate metric %s" % metric)
        _print_usage()
        exit(-1)

    try:
        output_yaml = yaml.safe_load(proc.stdout)
    except:
        print("Invalid yaml data from metric %s" % metric)
        _print_usage()
        exit(-1)

    return { metric: output_yaml }

def _export_results(metric_results, taskname):
    # Build the final yaml structure and save it to the result.yml file.
    results_yaml = {
        "task": os.environ["%s_NAME" % taskname.upper()],
        "students": "", # TODO: Implement extra script for this
        "tests": metric_results
    }

    result_yml_path = "../results/%s/result.yml" % taskname
    os.makedirs(os.path.dirname(result_yml_path), exist_ok=True)
    with open(result_yml_path, "w") as file:
        yaml.dump(results_yaml, file)

def _main():
    taskname = "task"
    if sys.argv == 2:
        taskname = sys.argv[1]

    metrics = _get_metrics_list(taskname)
    tests = []
    for metric in metrics:
        tests.append(_evaluate_metric(metric, taskname))
    _export_results(tests, taskname)

if __name__ == "__main__":
    _main()
