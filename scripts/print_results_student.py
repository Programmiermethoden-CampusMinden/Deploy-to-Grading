#!/bin/python3

# Prints a summary of the assignment results to the console for the students.
# The results are printed when executing the Deploy-to-Grading pipeline locally
# as well as in the console of the GitHub Action.
# Before executing this script, please make sure that all results have been
# exported to the results/ folder in the root directory of the assignment and
# that the assignment configuration has been loaded into the environment variables.
#
# usage: print_results_student.py
#

from datetime import datetime
import os
import result_utils

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
        points = result_utils.get_points_of_task(results[task])
        print(("| {:<%d}|{:>%d} |" % (max_taskname_length-1, points_length-1))
            .format(task, "%d/%d" % points))
    print("+%s+%s+" % ('-'*max_taskname_length, '-'*points_length))

def _print_deductions(results):
    # Prints deductions of every metric of every task to the console.
    for task in results:
        for metric in results[task][1]["tests"]:
            if "mistakes" in metric[list(metric.keys())[0]]:
                for mistake in metric[list(metric.keys())[0]]["mistakes"]:
                    print("[%s:%s (-%.2f Punkt(e))] %s"
                        % (task, list(metric.keys())[0], mistake["deduction"],
                        mistake["description"]))

def _main():
    results = result_utils.load_yaml_results(os.environ["ASSIGNMENT_TASKS"].split(" "))

    print("")
    # We print deductions before the final results because the we want the students
    # to see the final results before the deductions.
    _print_deductions(results)
    print("")
    print("Aufgabenblatt: %s" % os.environ["ASSIGNMENT_NAME"])
    print("Abgabedatum: %s" % _format_date(os.environ["ASSIGNMENT_DUE_DATE"]))
    print("Beteiligte Studis: %s" % ", ".join(_get_students_involved(results)))
    print("Erreichte Punktzahl: %d/%d" % result_utils.get_overall_points(results))
    print("")
    _print_task_results_table(results)

if __name__ == "__main__":
    _main()
