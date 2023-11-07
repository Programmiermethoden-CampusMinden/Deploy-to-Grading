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

def has_env_variable(key, taskname=None):
    """
    Combines taskname with key and checks if an environment variable with
    the given name is defined.

    Params:
    key      (string): Key of the environment variable.
    taskname (string): Optional taskname that is combined with the env key.

    Returns:
    bool: True when the environment variable exists.
    """
    if taskname is not None:
        key = key % taskname.upper()

    return key in os.environ

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

def create_mistake(deduction, description):
    """
    Creates a new mistake object containing the deduction points and a
    description of the error.

    Params:
    deduction   (number): Number of points that are deducted from the overall
                          because of the mistake.
    description (string): Description of the mistake containing information
                          about what is wrong and where the mistake is.

    Returns:
    dict: mistake object containing the summary of the mistake.
    """
    return {
        "deduction": deduction,
        "description": description
    }

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
        results["mistakes"] = [create_mistake(points, error_description)]
  
    # Note: We do not use the default function here as we don't want that the
    # "mistakes" variable is defined in the final dictionary.
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
    return generate_final_results(
        mistakes,
        max(max_points - len(mistakes*deduction_per_error), 0),
        max_points
    )

def generate_final_results(mistakes, points, max_points):
    """
    Default function for generating the final results.
    
    Params:
    mistakes     (list): List of mistakes as defined in
                         d2g_procedure.md in the documentation.
    points     (number): Number of points for all correct answers.
    max_points (number): Maximum number of points that can be achieved.
    
    Returns:
    dict: final results for dumping as yaml
    """
    results = {
        "points": points,
        "max_points": max_points,
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
