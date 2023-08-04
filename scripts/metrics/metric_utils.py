# Python module containing utility functions for metric evaluation.

import os
import sys
import xml.etree.ElementTree as ET
import yaml

def get_taskname():
    """
    Gets taskname from argv and returns it. If taskname was not set, it
    returns "task" as a default.

    Returns:
    string: Name of the task used e.g. as part of paths
    """
    taskname = "task"
    if len(sys.argv) == 2:
        taskname = sys.argv[1]
    return taskname

def print_usage(usage_text):
    """
    Prints usage information to the console.

    Params:
    usage_text (string): String containing usage information.
    """
    if usage_text is not None:
        print(usage_text)

def get_env_variable(key, taskname=None, usage_text=None):
    """
    Combines taskname with key and returns its corresponding environment
    variable. If the environment variable is not set, the functions exits
    the program with an error.

    Params:
    key        (string): Key of the environment variable.
    taskname   (string): Optional taskname that is combined with the env key.
    usage_text (string): Optional usage text printed when the environment
                         variable is not set.

    Returns:
    string: Value of the environment variable.
    """
    if taskname is not None:
        key = key % taskname.upper()

    if os.getenv(key) is None:
        print("Environment variable %s not defined" % key)
        print_usage(usage_text)
        exit(-1)

    return os.getenv(key)

def load_xml_file(path, usage_text=None):
    """
    Loads the xml file given by path. If the file cannot be loaded, the function
    exits the program with an error.

    Params:
    path       (string): Path to the xml file.
    usage_text (string): Optional usage text printed when the environment
                         variable is not set.

    Returns:
    ElementTree: Object containing xml data.
    """
    try:
        return ET.parse(path)
    except ET.ParseError as err:
        print("Invalid xml file %s" % path)
    except FileNotFoundError as err:
        print("File %s not found" % path)
    # The following lines are only reached on error.
    print(usage_text)
    exit(-1)

def load_yaml(path, usage_text=None):
    """
    Loads the yaml file given by path. If the file cannot be loaded, the function
    exits the program with an error.

    Params:
    path       (string): Path to the yaml file.
    usage_text (string): Optional usage text printed when the environment
                         variable is not set.

    Returns:
    dict: Dictionary containing yaml data.
    """
    try:
        with open(path, "r") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError:
                print("Invalid yaml file %s" % path)
                print(usage_text)
                exit(-1)
    except FileNotFoundError as err:
        print("File %s not found" % path)
        print(usage_text)
        exit(-1)

def generate_final_results_all_or_nothing(result, points, error_description):
    """
    Generates a results dictionary as defined in d2g_procedure.md in the
    documentation for the all or nothing strategy that either grants all
    or no points.
    
    Params:
    result              (bool): True when the task has been solved correctly.
    points            (number): Amount of points to grant when the task has
                                been solved correctly.
    error_description (string): Description of the mistake when the task was
                                not solved correctly.
    
    Returns:
    dict: final results for dumping as yaml
    """
    results = {
        "points": points if result else 0,
        "max_points": points
    }

    if not result:
        results["mistakes"] = [
            {
                "deduction": points,
                "description": error_description
            }
        ]

    return results

def generate_final_results_deduction_per_error(
        mistakes, max_points, deduction_per_error):
    """
    Generates a results dictionary as defined in d2g_procedure.md in the
    documentation for the deduction per error strategy that deducts points
    per mistake up to a maximum number of points.

    Params:
    mistakes              (list): List of mistakes as defined in
                                  d2g_procedure.md in the documentation.
    max_points          (number): Maximum number of points that can be reached.
    deduction_per_error (number): Number of points that are deducted per error.
    
    Returns:
    dict: final results for dumping as yaml
    """
    results = {
        "points": max(max_points - len(mistakes*deduction_per_error), 0),
        "max_points": max_points,
        "mistakes": mistakes
    }

    return results

def generate_final_results_points_per_test(
        mistakes, test_count, points_per_test):
    """
    Generates a results dictionary as defined in d2g_procedure.md in the
    documentation for the points per test strategy that grants a defined
    number of points for each correct test.

    Params:
    mistakes          (list): List of mistakes as defined in
                              d2g_procedure.md in the documentation.
    test_count       (tuple): Tuple (all_tests, failed_tests) containing
                              the number of tests executed and the number of
                              tests that failed.
    points_per_test (number): Points awarded per correct test.
    
    Returns:
    dict: final results for dumping as yaml
    """
    results = {
        "points": (test_count[0]-test_count[1]) * points_per_test,
        "max_points": test_count[0] * points_per_test,
        "mistakes": mistakes
    }

    return results

def print_results(results):
    """
    Prints results to the console as yaml.
    
    Params:
    results (dict): string containing yaml data of the results
    """
    print(yaml.dump(results), end="")
