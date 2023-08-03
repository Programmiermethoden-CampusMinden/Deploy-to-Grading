#!/bin/python3

from datetime import datetime
import load_yaml as yaml_loader
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

def _load_yaml_results(tasks):
    # Load the results for every task. Returns a dictionary containing
    # a tuple of task configuration and result for every task.
    results = {}
    for task in tasks:
        results[task] = _load_yaml_result_for_task(task)
    return results

def _format_date(date):
    # Format date in the format "%Y-%m-%dT%H:%M" to the more
    # human-readable format "%d.%m.%Y %H:%M".
    datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M")
    return datetime_obj.strftime("%d.%m.%Y %H:%M")

def _get_students_involved(results):
    # Get a list of students involved in this assignment.
    students = set()
    for task in results:
        students.update(results[task][1]["students"])
    return list(students)

def _get_points_of_task(task):
    # Get points achieved in a single task. Returns a tuple of
    # (reached_points, max_points).
    points = 0
    max_points = 0
    for metric in task[1]["tests"]:
        points += metric[list(metric.keys())[0]]["points"]
        max_points += metric[list(metric.keys())[0]]["max_points"]

    return (points, max_points)

def _get_overall_points(results):
    # Get overall points achieved in this assignment. Returns a tuple
    # of (reached_points, max_points).
    overall_points = 0
    max_points = 0

    for task in results:
        points = _get_points_of_task(results[task])
        overall_points += points[0]
        max_points += points[1]

    return (overall_points, max_points)

def _get_longest_task_name(tasknames):
    # Get length of the longest task name.
    max_length = 0
    for name in tasknames:
        if len(name) > max_length:
            max_length = len(name)
    return max_length

def _print_task_results_table(results):
    # Pretty print results for each task in a table. We don't import a module
    # for this as the module would need to be installed. To make things easy,
    # we do it without the module.
    max_taskname_length = _get_longest_task_name(results.keys())+2
    points_length = len("Punkte")+2
    print("+%s+%s+" % ('-'*max_taskname_length, '-'*points_length))
    print(("| {:<%d}| {:<%d}|" % (max_taskname_length-1, points_length-1))
        .format("Aufgabe", "Punkte"))
    print("+%s+%s+" % ('-'*max_taskname_length, '-'*points_length))
    for task in results:
        points = _get_points_of_task(results[task])
        print(("| {:<%d}|{:>%d} |" % (max_taskname_length-1, points_length-1))
            .format(task, "%d/%d" % points))
    print("+%s+%s+" % ('-'*max_taskname_length, '-'*points_length))

def _print_deductions(results):
    for task in results:
        for metric in results[task][1]["tests"]:
            if "mistakes" in metric[list(metric.keys())[0]]:
                for mistake in metric[list(metric.keys())[0]]["mistakes"]:
                    print("[%s:%s (-%d Punkt(e))] %s"
                        % (task, list(metric.keys())[0], mistake["deduction"],
                        mistake["description"]))

def _main():
    results = _load_yaml_results(os.environ["ASSIGNMENT_TASKS"].split(" "))

    print("")
    _print_deductions(results)
    print("")
    print("Aufgabenblatt: %s" % os.environ["ASSIGNMENT_NAME"])
    print("Abgabedatum: %s" % _format_date(os.environ["ASSIGNMENT_DUE_DATE"]))
    print("Beteiligte Studis: %s" % ", ".join(_get_students_involved(results)))
    print("Erreichte Punktzahl: %d/%d" % _get_overall_points(results))
    print("")
    _print_task_results_table(results)

if __name__ == "__main__":
    _main()
