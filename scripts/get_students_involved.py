# TODO
#
# Also detects 'Not commited yet' as a user. We ignore this as it should not
# happend when using the Deploy-to-Grading pipeline inside a GitHub Action
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

    # Clone repo (Only if it has not been cloned before)
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

def _get_authors_of_file(file):
    # Gets all authors of a file using git blame
    authors = set()

    # Setting date format to unix so that we don't have to parse as many whitespaces
    proc = subprocess.run(["git", "blame", "--date=unix", file], capture_output=True)
    if proc.returncode == 0:
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
    # Determine all students involved in this task using git blame. Returns
    # a list containing the students names.
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
    print(list(students))

    return list(students)
