# Collects all students that participated in a given task. It clones the
# template repository and determines all files that are present in the students
# repository but not in the template repository. For every file determined the
# authors are determined using git blame. The ASSIGNMENT_TEMPLATE_REPOSITORY
# env variable needs to be set to the template repository.
#
# usage:
# ```python
# import .get_students_involved as students
# 
# authors = students.get_students_involved(taskname)
# ```
#
# Note: This script also detects 'Not commited yet' as a user. We ignore this
# as it should not happend when using the Deploy-to-Grading pipeline inside
# a GitHub Action.
#

import os
import subprocess
import shutil

DIR_PREFIX = "template/"

def _get_repository_name(url):
    # Extract repository name from the url
    size = len(url)
    start = size - url[size:0:-1].index('/', 0, size)
    return url[start:size]

def _clone_template_repository(url):
    # Clone the repository to DIR_PREFIX/REPO_NAME if it has not
    # been cloned yet.
    repo_name = _get_repository_name(url)

    if not os.path.isdir(DIR_PREFIX):
        os.mkdir(DIR_PREFIX)

    current_dir = os.getcwd()
    os.chdir(DIR_PREFIX)
    return_code = subprocess.call(["git", "clone", "--depth", "1", url])
    os.chdir(current_dir)
    
    if return_code != 0:
        print("Failed to clone template repository.")
        return False
    return True

def _get_template_files(template_repository):
    # Collect a list of all files inside the template repository.
    template_files = []
    repo_name = _get_repository_name(template_repository)
    template_repo_path = os.path.join(DIR_PREFIX, repo_name)

    for path, _, files in os.walk(template_repo_path):
        for file in files:
            template_files.append(
                os.path.join(path, file)[len(template_repo_path)+1:])

    return template_files

def _get_files_to_check(template_files):
    # Get all files in the selected task that are not part of the template
    # repository.
    # TODO: Currently ignores the %TASKNAME%_NO_OVERRIDE setting as these
    # files can contain changes by the template authors and we don want
    # them to be listed in the authors set.
    files_to_check = []
    for path, _, files in os.walk("."):
        for file in files:
            full_path = os.path.join(path, file)
            # Check if file is not a template file
            if not full_path in template_files:
                files_to_check.append(full_path)

    return files_to_check

def _get_author_of_line(blame_line):
    # Extracts the author name from the git blame line.
    name_start = blame_line.find("(")+1
    closed_bracket_index = blame_line.find(")")
    split_line_part = blame_line[name_start:closed_bracket_index].split()
    return " ".join(split_line_part[:len(split_line_part)-2])

def _is_binary_file(file_path):
    # Checks if file is binary
    try:
        with open(file_path, "r") as file:
            # Only read first 512 bytes as these should be enough to detect
            # a binary file.
            data = file.read(512)
            
            # We treat empty files as text files
            if len(data) == 0:
                return False
            
            # Since binary files typically contain zero, this should be enough
            # to detect binary files.
            if '\x00' in data:
                return True

            return False
    except:
        # If reading fails, the file is binary. Since we don't try to read in
        # binary mode.
        return True

def _get_authors_of_file(file):
    # Gets all authors of a file using git blame
    authors = set()

    # Setting date format to unix so that we don't have to parse as many whitespaces
    proc = subprocess.run(["git", "blame", "--date=unix", file], capture_output=True)
    if proc.returncode == 0:
        # Because of issues with line breaks we need to handle binary files
        # differently.
        if _is_binary_file(file):
            # Only add author of "first line" of the binary file
            authors.add(_get_author_of_line(str(proc.stdout.splitlines()[0])))
        else:
            # Get authors for every line of a text file
            for line in proc.stdout.splitlines():
                authors.add(_get_author_of_line(str(line)))
    elif proc.returncode == 128:
        # Error 128 seems to indicate that the file is ignored by git
        pass

    return authors

def _get_authors_of_task(files_to_check):
    # Iterate over all files of the repository and gets their authors.
    authors = set()

    for file in files_to_check:
        authors.update(_get_authors_of_file(file))

    return authors

def _cleanup(repository):
    # Deletes the previously cloned repository.
    repo_name = _get_repository_name(repository)
    shutil.rmtree(os.path.join(DIR_PREFIX, repo_name))

def get_students_involved(taskname):
    """
    Determine all students involved in this task using git blame. Requires
    the ASSIGNMENT_TEMPLATE_REPOSITORY to be set to a valid template
    repository.

    Parameters:
    taskname (string): Name of the task to determine the students for

    Returns:
    list: Student names as strings
    """
    students = []

    template_repository = os.getenv("ASSIGNMENT_TEMPLATE_REPOSITORY")
    if not template_repository:
        print("Template repository not set")
        return []

    if not _clone_template_repository(template_repository):
        return []

    template_files = _get_template_files(template_repository)

    files_to_check = _get_files_to_check(template_files)
    students = _get_authors_of_task(files_to_check)

    _cleanup(template_repository)

    return list(students)
