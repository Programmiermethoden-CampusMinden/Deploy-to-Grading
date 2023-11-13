#!/bin/python3

import zipfile
import json

# Script for evaluating the JPlag plagiarism check. It counts the number of
# detected plagiarised comparisons and prints them to the console output.
#
# usage: jplag_eval.py
#
# Make sure that the jplag.sh script has been executed prior to this script.
#

ZIP_PATH = "jplag/jplag_results.zip"
JSON_PATH = "overview.json"

# Treat similarity scores above 70% as plagiarism. Value means 10%-steps from
# 100% downwards
DEFAULT_PLAGIARISM_PERECENTAGE = 3 # Equals 100% - 70%

# We use AVG as the default metric as this seems to be the metric that is seems
# to be the default value used on their official website as well.
EVALUATED_METRIC = "AVG" # Possible values AVG, MAX

def _print_results(metric):
    # Print number of comparisons that have a higher similarity than the
    # configured DEFAULT_PLAGIARISM_PERECENTAGE
    plagiarised_comparisons = 0

    # Count plagiarised comparisons
    i = 0
    while i < DEFAULT_PLAGIARISM_PERECENTAGE \
            and i < len(metric["distribution"]):
        plagiarised_comparisons += metric["distribution"][i]
        i += 1

    print_value = plagiarised_comparisons if plagiarised_comparisons > 0 \
        else "no"
    print("JPlag detected %s plagiarism(s)." % print_value)

def _main():
    # Open overview.json in zip file.
    try:
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip:
            with zip.open(JSON_PATH) as json_file:
                # Search for the metric we want to show the results for.
                for metric in json.load(json_file)["metrics"]:
                    if metric["name"] == EVALUATED_METRIC:
                        _print_results(metric)
    except FileNotFoundError:
        print("No JPlag results found. Has it been executed?")
    except KeyError:
        print(f"Error detected in executing JPlag. Missing {JSON_PATH}.")


if __name__ == "__main__":
    _main()
