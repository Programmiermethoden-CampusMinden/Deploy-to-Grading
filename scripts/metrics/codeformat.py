#!/bin/python3

# Executes the codeformat metric and evaluates its results. This script stores
# the results in "build/results/codeformat.yml" and converts them into the
# "results.yml" format defined in the 
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

import metric_utils
import os
import sys

RESULTS_DIR = "build/results/"
RESULT_FILE = "codeformat.yml"

POINTS_ENV_KEY = "%s_METRICS_CODEFORMAT_POINTS"

USAGE = """usage: codeformat_eval.py [taskname(optional)]
       Make sure that codeformat.sh was executed prior to this
       script and that the task yaml was loaded correctly.

       Params:
       taskname    Prefix of the task used for env variables.
"""

def _main():
    taskname = "task"
    if len(sys.argv) == 2:
        taskname = sys.argv[1]

    # Execute metric
    returncode = metric_utils.execute_metric("./gradlew spotlessJavaCheck")
    metric_utils.save_metric_result("codeformat", returncode)

    # Evaluate and save results
    data = metric_utils.load_yaml(
        os.path.join(RESULTS_DIR, RESULT_FILE), USAGE)
    points = int(metric_utils.get_env_variable(
        POINTS_ENV_KEY, taskname, USAGE))
    results = metric_utils.generate_final_results_all_or_nothing(
        data["result"] == 0, points, "The code is not formatted correctly. \
Please format your code using spotless.")
    metric_utils.print_results(results)    

if __name__ == "__main__":
    _main()
