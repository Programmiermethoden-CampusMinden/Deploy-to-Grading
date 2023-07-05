#!/bin/python3

import argparse
import os
import subprocess
import shutil

TEMPLATE_REPO_URL_KEY = "ASSIGNMENT_TEMPLATE_REPOSITORY"
DEFAULT_TEMPLATE_REPO_URL = "https://github.com/akirsch1/d2g-dummy-template"

DIR_PREFIX = "template/"

DEFAULT_NO_OVERRIDE = [".git/"]

def _print_usage():
    print("Execute override_repo.py -h to print usage information.")
    exit(-1)

def _parse_args():
    # Parse taskname, repository and no_override args. For more
    # information, see override_repo.py -h

    # Create arg parser with options --taskname and --repository
    parser = argparse.ArgumentParser(
        prog="override_repo.py",
        description="Override all template files using the files from the \
            parent repository to revert changes made by students.\n \
            Use TASK_NO_OVERRIDE environment variable to declare files that \
            should not be overriden.")
    parser.add_argument("-t", "--taskname",
        action="store", default="task",
        help="Name of the task used as env variable prefix.")
    parser.add_argument("-r", "--repository",
        action="store",  default= os.getenv(TEMPLATE_REPO_URL_KEY)
            if TEMPLATE_REPO_URL_KEY in os.environ
            else DEFAULT_TEMPLATE_REPO_URL,
        help="URL used for cloning the template repository.")
    args = parser.parse_args()

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
    if not os.path.isdir(DIR_PREFIX+repo_name):
        if not os.path.isdir(DIR_PREFIX):
            os.mkdir(DIR_PREFIX)
        current_dir = os.getcwd()
        os.chdir(DIR_PREFIX)
        return_code = subprocess.call(["git", "clone", "--depth", "1", url])
        os.chdir(current_dir)
        if return_code != 0:
            print("Failed to clone template repository.")
            _print_usage()
    # TODO: It might be useful to only figure out the last shared commit
    # and update the files based on that commit. Currently two template
    # versions will be mixed if the student repository is not up-to-date.
    # TODO: git pull might be necessary when the repository already exists

def _is_ignored(filepath, no_override):
    # Check if a file or filepath is ignored and should not be overriden.
    # Returns true when it should NOT be overriden.
    for ignored in no_override:
        if (ignored.endswith("/") and filepath.startswith(ignored)) \
                or filepath == ignored:
            return True
    return False

def _override_files(taskname, repository, no_override):
    repo_name = _get_repository_name(repository)

    # Loop through all files including files in subdirectories
    template_repo_path = os.path.join(DIR_PREFIX, repo_name)
    for path, _, files in os.walk(template_repo_path):
        for file in files:
            filepath = os.path.join(path, file)
            # Copy the file when it is not ignored two folders up
            if not _is_ignored(filepath[len(template_repo_path)+1:], no_override):
                shutil.copyfile(filepath, filepath[len(template_repo_path)+1:])

def _cleanup(repository):
    # Deletes the previously cloned repository.
    # TODO: Implement. When doing this, the cloning check can be removed
    pass

def _main():
    args = _parse_args()
    _clone_template_repository(args.repository)
    _override_files(args.taskname, args.repository, args.no_override)
    _cleanup(args.repository)

if __name__ == "__main__":
    _main()

