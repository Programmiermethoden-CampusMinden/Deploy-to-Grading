#!/bin/python3

import os
import subprocess
import sys
import yaml

def _print_usage():
    print("usage: evaluate_task.py [taskname(optional)]")
    print("       Requires that environment variable *TASKNAME*_METRICS is set.")
    exit(-1)

def _get_metrics_list(taskname):
    # Load a list of all metrics used in this task. The list is loaded
    # from the environment variable *TASKNAME*_METRICS.
    metrics_string = os.environ["%s_METRICS" % taskname.upper()]

    if not metrics_string or metrics_string == "":
        _print_usage()

    return metrics_string.split(" ")

def _evaluate_metric(metric, taskname):
    # Execute the evaluation script of the given metric and return its
    # output as yaml.

    proc = subprocess.run(["%s/scripts/metrics/%s_eval.py" % \
        (os.environ["D2G_PATH"], metric), taskname], capture_output=True)
    if proc.returncode != 0:
        print("Failed to evaluate metric %s" % metric)
        _print_usage()

    try:
        output_yaml = yaml.safe_load(proc.stdout)
    except:
        print("Invalid yaml data from metric %s" % metric)
        _print_usage()

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
