# Python module containing utility functions for yaml result file parsing.

import math
import os
import yaml

TASK_FILENAME = "task.yml"
RESULT_FILENAME = "result.yml"

RESULTS_FOLDER = "results/"

def _load_yaml_result_for_task(taskname):
    # Load the results for a given task. Reads both the result.yml and
    # task.yml configuration for the task. Return a tuple containing
    # (task_configuration, results).
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

def load_yaml_results(tasks):
    """
    Loads the results for every given task.

    Params:
    tasks  (string[]): List of task names.

    Returns:
    dict: Dictionary containing a tuple of task configuration and result for
          every task.
    """
    results = {}
    for task in tasks:
        results[task] = _load_yaml_result_for_task(task)
    return results

def get_points_of_task(task):
    """
    Get points achieved in a single task.

    Params:
    task       (list): Task object as loaded by "load_yaml_results".

    Returns:
    tuple: Tuple of (reached_points, max_points).
    """
    points = 0
    max_points = 0
    for metric in task[1]["tests"]:
        # We round up here because we don't want to deduct non-full points.
        points += math.ceil(metric[list(metric.keys())[0]]["points"])
        max_points += metric[list(metric.keys())[0]]["max_points"]

    return (points, max_points)

def get_overall_points(results):
    """
    Gets overall points achieved in an assignment.

    Params:
    results  (string): Results object as loaded by "load_yaml_results".

    Returns:
    tuple: Tuple of (overall_points, max_points).
    """
    overall_points = 0
    max_points = 0

    for task in results:
        points = get_points_of_task(results[task])
        overall_points += points[0]
        max_points += points[1]

    return (overall_points, max_points)
