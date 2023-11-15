#!/bin/python3

# Copies all files from a template repository to the current repository.
# This script is used to prevent changes from students in files they are
# not allowed to change. Files that are present in the current repository
# as well as the template repository and that should not be overridden
# need to be listed in the configuration file of the current task. Check
# the [documentation](https://github.com/Programmiermethoden/Deploy-to-Grading/blob/master/doc/design_document/repository_structure/task_and_assignment_structure.md#format-aufgabendefinition-taskyml)
# on how to define files that should not be overwritten. Furthermore, it
# checks for differences in the config files. The execution fails, if it
# detects any changes.
# Make sure that the script is executed inside a task folder and that the
# task configuration was loaded correctly.
#
# usage: override_repo.py [-h] [-t TASKNAME] [-a] -r REPOSITORY
#  Params:
#  h, help:        Show a help message and exit
#  t, taskname:    Name of the task used as env variable prefix
#  a, assignment:  Set to true, if only the difference in assignment.yml
#                  should be checked
#  r, repository:  URL used for cloning the template repository
#
# Error handling:
# - Exits with an error code when it fails to clone the given repository.
#
# This script is step 4 in the Deploy-to-Grading pipeline and is executed
# once for every task.
#

import argparse
import os
import subprocess
import shutil

TEMPLATE_REPO_URL_KEY = "ASSIGNMENT_TEMPLATE_REPOSITORY"
DIR_PREFIX = "../template/"
DEFAULT_NO_OVERRIDE = [".git/"]

TASK_CONFIG_FILENAME = "task.yml"
ASSIGNMENT_CONFIG_FILENAME = "assignment.yml"

def _create_arg_parser():
    # Create a new argumen parser and returns it
    parser = argparse.ArgumentParser(
        prog="override_repo.py",
        description="""Override all template files using the files from the
            parent repository to revert changes made by students.\n
            Use TASK_NO_OVERRIDE environment variable to declare files that
            should not be overriden.""")
    parser.add_argument("-t", "--taskname",
        action="store", default="task",
        help="Name of the task used as env variable prefix.")
    parser.add_argument("-a", "--assignment",
        action="store_true",
        help="Set to true, if only the difference in assignment.yml should be checked.")
    parser.add_argument("-r", "--repository",
        action="store", required=True,
        help="URL used for cloning the template repository.")
    return parser

def _parse_args():
    # Parse taskname, repository and no_override args. For more
    # information, see override_repo.py -h
    args = _create_arg_parser().parse_args()

    # Load all no_override files from the environment variable
    no_override_string = os.getenv("%s_NO_OVERRIDE" % args.taskname.upper())
    if no_override_string is not None:
        args.no_override = no_override_string.split(" ")
    else:
        args.no_override = []
    args.no_override += DEFAULT_NO_OVERRIDE

    return args

def _get_repository_name(url):
    # Extract repository name from the url
    size = len(url)
    start = size - url[size:0:-1].index('/', 0, size)
    return url[start:size]

def _clone_template_repository(url):
    # Clone the repository to DIR_PREFIX/REPO_NAME if it has not
    # been cloned yet.
    repo_name = _get_repository_name(url)

    # Clone repo (Only if it has not been cloned before)
    if not os.path.isdir(DIR_PREFIX):
        os.mkdir(DIR_PREFIX)

    current_dir = os.getcwd()
    os.chdir(DIR_PREFIX)
    return_code = subprocess.call(["git", "clone", "--depth", "1", url])
    os.chdir(current_dir)
    
    if return_code != 0:
        print("Failed to clone template repository.")
        _create_arg_parser().print_help()
        exit(-1)

def _is_ignored(filepath, no_override):
    # Check if a file or filepath is ignored and should not be overriden.
    # Returns true when it should NOT be overriden.
    for ignored in no_override:
        if (ignored.endswith("/") and filepath.startswith(ignored)) \
                or filepath == ignored:
            return True
    return False

def _check_for_config_change(taskname, repository):
    # Compares the config in the student repository with the same
    # config in the template repository. Exit with an error, if they do not
    # have the same content

    # Create the paths to the config files. Differentiate between task.yml
    # and assingment.yml. The assignment.yml is checked, if the filename is
    # None.
    student_config_path = ASSIGNMENT_CONFIG_FILENAME if taskname is None \
        else TASK_CONFIG_FILENAME
    repo_name = _get_repository_name(repository)
    template_config_path = None
    if taskname is None:
        template_config_path = os.path.join(DIR_PREFIX, repo_name, \
            ASSIGNMENT_CONFIG_FILENAME)
    else:
        template_config_path = os.path.join(DIR_PREFIX, repo_name, taskname,
            TASK_CONFIG_FILENAME)

    # We assume that both the student config as well as the template config
    # do exist here, since deploy-to-grading would have failed earlier in
    # case of the student_config. In case of the template_config, the template
    # repository is not configured correctly, which we don't want to handle
    # here.
    with open(student_config_path) as student_config, \
            open(template_config_path) as template_config:
        student_content = student_config.read()
        template_content = template_config.read()

        # Compare the content of the file. Fail, if it is not the same.
        if student_content != template_content:
            if taskname is None:
                print(f"Student config and template assignment config"+
                    " are not matching. Has the student config been edited?")
            else:
                print(f"Student config and template config in {taskname}"+
                    " are not matching. Has the student config been edited?")
            _cleanup()
            exit(-1)


def _override_files(taskname, repository, no_override):
    # Override all template files that are not listed in no_override
    repo_name = _get_repository_name(repository)

    # Loop through all files including files in subdirectories
    template_repo_path = os.path.join(DIR_PREFIX, repo_name, taskname)
    for path, _, files in os.walk(template_repo_path):
        for file in files:
            filepath = os.path.join(path, file)
            # Copy the file when it is not ignored two folders up
            if not _is_ignored(filepath[len(template_repo_path)+1:], no_override):
                shutil.copyfile(filepath, filepath[len(template_repo_path)+1:])

def _cleanup():
    # Deletes the previously cloned repository.
    shutil.rmtree(DIR_PREFIX)

def _main():
    args = _parse_args()
    _clone_template_repository(args.repository)
    _check_for_config_change(None if args.assignment else args.taskname,
        args.repository)
    if (not args.assignment):
        _override_files(args.taskname, args.repository, args.no_override)
    _cleanup()

if __name__ == "__main__":
    _main()

