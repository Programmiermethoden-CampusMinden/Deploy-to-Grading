#!/bin/python3

import load_yaml as yaml_loader
import os
import yaml

TASK_FILENAME = "task.yml"
RESULT_FILENAME = "result.yml"

RESULTS_FOLDER = "results/"

def _load_yaml_result_for_task(taskname):
    task_conf = None
    result = None
    task_conf_path = os.path.join(RESULTS_FOLDER, taskname, TASK_FILENAME)
    result_path = os.path.join(RESULTS_FOLDER, taskname, RESULT_FILENAME)

    with open(task_conf_path, "r") as task_conf_file:
        try:
            task_conf = yaml.safe_load(task_conf_file)
        except yaml.YAMLError:
            print("Failed to load config for task %s" % taskname)

    with open(result_path, "r") as result_file:
        try:
            result = yaml.safe_load(result_file)
        except yaml.YAMLError:
            print("Failed to load results for task %s" % taskname)
    
    return (task_conf, result)

def _load_yaml_results(tasks):
    results = {}
    for task in tasks:
        results[task] = _load_yaml_result_for_task(task)
    return results

def _main():
    results = _load_yaml_results(os.environ["ASSIGNMENT_TASKS"].split(" "))

    print(results)

if __name__ == "__main__":
    _main()
