#!/bin/python3

import load_yaml as conf_loader
import os
import subprocess
from yaml import YAMLError

ASSIGNMENT_FILE_NAME = "assignment.yml"
TASK_FILENAME = "task.yml"

def _print_usage():
    print("usage: deploy_to_grading.py")
    print("       Executes the Deploy-to-Grading pipeline.")

def _print_error_and_exit(error_msg):
    print(error_msg)
    _print_usage()
    exit(-1)

def _load_assignment_config():
    # Step 1 of the Deploy-to-Grading pipeline
    try:
        return conf_loader.load_yaml(ASSIGNMENT_FILE_NAME)
    except (FileNotFoundError, YAMLError) as err:
        _print_error_and_exit("Failed to load %s" % ASSIGNMENT_FILE_NAME)

def _checkout_due_date(due_date):
    # Step 2 of the Deploy-to-Grading pipeline
    script_path = os.path.join(os.environ["D2G_PATH"],
        "scripts/checkout_due_date.sh")
    proc = subprocess.run([script, due_date])
    if proc.returncode != 0:
        _print_error_and_exit("Failed to evaluate checkout commit")

def _load_task_config(taskname):
    # Step 3 of the Deploy-to-Grading pipeline
    task_config_path = os.path.join(taskname, TASK_FILENAME)
    try:
        return conf_loader.load_yaml(task_config_path)
    except (FileNotFoundError, YAMLError) as err:
        _print_error_and_exit("Failed to load %s" % task_config_path)

def _override_repo(taskname, repository, no_override):
    # Step 4 of the Deploy-to-Grading pipeline
    script_path = os.path.join(os.environ["D2G_PATH"],
        "scripts/override_repo.py")
    proc = subprocess.run(
        [script_path, "-t", taskname, "-r", repository], cwd=taskname)
    if proc.returncode != 0:
        _print_error_and_exit("Failed to execute override_repo.py")

def _get_metric_script_path(metric):
    # Search for an evaluation script for the given metrics. Looks for 
    # scripts written in bash or python. If such a script does not exist,
    # it assumes that the metric is a gradle task.
    base_path = os.path.join(os.environ["D2G_PATH"],
        "scripts/metrics/%s" % metric)
    if os.path.exists(base_path + ".sh"):
        return [base_path + ".sh"]
    elif os.path.exists(base_path + ".py"):
        return [base_path + ".py"]
    else:
        return ["./gradlew", metric]

def _execute_metrics(taskname, metrics):
    # Runs step 5 of the Deploy-to-Grading pipeline for every metric
    for metric in metrics:
        metric_script = _get_metric_script_path(metric)

        proc = subprocess.run([metric_script], cwd=taskname)
        if proc.returncode != 0:
            _print_error_and_exit("Failed to execute metric %s" % metric)

def _evaluate_metrics(taskname, metrics, task_configuration):
    # Step 6 fo the Deploy-to-Grading pipeline
    script_path = os.path.join(os.environ["D2G_PATH"],
        "scripts/evaluate_task.py")
    proc = subprocess.run([script_path], cwd=taskname, env=task_configuration)
    if proc.returncode != 0:
        _print_error_and_exit("Failed to execute override_repo.py")

def _evaluate_task(taskname, repository):
    # Runs step 3 to 6 of the Deploy-to-Grading pipeline
    task_conf = _load_task_config(taskname)
    override_repo(taskname, repository, task_conf["%s_NO_OVERRIDE" % taskname])
    _execute_metrics(taskname, task_conf["%s_METRICS" % taskname])
    _evaluate_metrics(taskname, task_conf["%s_METRICS" % taskname], task_conf)

def _main():
    assignment_conf = _load_assignment_config()
    _checkout_due_date(assignment_conf["ASSIGNMENT_DUE_DATE"])

    for task in assignment_conf["ASSIGNMENT_TASKS"]:
        _evaluate_task(task, assignment_conf["ASSIGNMENT_TEMPLATE_REPOSITORY"])

    # TODO: Add step 7 (result presentation) of pipeline here

if __name__ == "__main__":
    main()
