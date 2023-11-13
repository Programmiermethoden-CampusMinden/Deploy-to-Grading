#!/bin/python3

import load_yaml as yaml_loader
import os
import pandas as pd
from github import Github, GithubException
import result_utils
import subprocess
import sys

URL_COLUMN = "Textabgabe"
EXPORT_FILE = "submission_results.xlsx"
USAGE = """usage: deploy_to_grading_teacher.py [submission_file]
       Collect all submissions defined in the submission file and asses them.

       Params:
       submission_file Path to an excel file containing all student submissions
                       as defined by ILIAS
"""

PLAGIARISM_METRIC = "jplag"

### Set environment variable GITHUB_TOKEN to avoid reaching api limits.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
github = Github(GITHUB_TOKEN)

def _print_error_and_exit(error_msg):
    print(error_msg)
    print(USAGE)
    exit(-1)

def _read_submission_list():
    # Load the submissions from an excel file. The excel file needs to have the
    # columns "Vorname", "Nachname", "Textabgabe", "Benutzername", and "Datum
    # der letzten Abgabe". "Textabgabe" should contain links to GitHub pull
    # requests.

    # Exit if no file path was given as an argument.
    if len(sys.argv) != 2:
        _print_error_and_exit("Path to submission file not specified.")

    try:
        # Read file using pandas (so that we can use dataframes).
        df = pd.read_excel(sys.argv[1])
    except:
        _print_error_and_exit("Failed to read file " + sys.argv[1])

    # Combine first and last name to not mix up names in the next step.
    df["Name"] = df["Nachname"] + ", " + df["Vorname"]
    # Group data based on "Textabgabe" so that we don't have to evaluate
    # repositories twice.
    grouped_df = df.groupby(URL_COLUMN).agg({
        "Name": list,
        "Benutzername": list,
        "Datum der letzten Abgabe": "max"
    }).reset_index()

    print("Evaluating submissions from")
    print(grouped_df[["Name", URL_COLUMN]])
    return grouped_df

def _clone_repository(pr_url):
    # Clones a repository and checks out its submission branch based on the
    # pull request url given by pr_url. Returns the path to the repos that was
    # checked out. Returns None if it failed to clone and checkout the
    # repository.

    # Parse pr_url to get necessary data.
    parts  = pr_url.strip("/").split("/")
    username, repo_name, pr_number = parts[-4], parts[-3], parts[-1]

    # Get repo information from GitHub API.
    try:
        repo = github.get_user(username).get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))
    except GithubException as e:
        print(f"Failed to clone and checkout repo {username}/{repo_name}.")
        return None

    # Determine repository path and make sure that all parent folders exist.
    path = f"repos/{username}_{repo_name}/"
    repo_path = f"{path}{repo_name}/"
    os.makedirs(path, exist_ok=True)

    # Execute clone and checkout.
    subprocess.run(["git", "clone", repo.clone_url], cwd=path)
    subprocess.run(["git", "checkout", pr.head.ref], cwd=repo_path)
    
    return repo_path

def _execute_deploy_to_grading(repo_path):
    # Execute the deploy to grading pipeline inside the student repository.
    result = subprocess.run(
        [f"{os.getenv('D2G_PATH')}/scripts/deploy_to_grading.py"],
        cwd=repo_path
    )
    return result.returncode

def _collect_results(repo_path):
    # Collect overall points and task-specific points from the results from the
    # results folder of the student repository.

    # Load assignment yaml since we need the selected tasks from it.
    assignment_yaml = yaml_loader.load_yaml(repo_path + "results/assignment.yml")

    # Save current working directory
    cur_dir = os.getcwd()
    # We need to change directory here because results_utils work relativ to the
    # root directory of the student repository.
    os.chdir(repo_path)
    # Load all results
    yaml_results = result_utils.load_yaml_results(
        assignment_yaml["ASSIGNMENT_TASKS"].split(" "))
    # Directory can already be reverted back here.
    os.chdir(cur_dir)

    # Get a list of points for each task.
    task_points = {}
    for taskname in yaml_results:
        task_points[taskname] = (result_utils.get_points_of_task(yaml_results[taskname]))
    # Get overall points so we don't have to calculate it here.
    overall_points = result_utils.get_overall_points(yaml_results)

    return overall_points, task_points

def _evaluate_submission(submission):
    # Evaluate the submission locally. Returns success bool, the local path to
    # the student repository and the overall point results

    # Clone repository into subfolder and prepare it for evaluation.
    repo_path = _clone_repository(submission[URL_COLUMN])

    # Return if the student repository could not be prepared.
    if not repo_path:
        return False, None, None
    
    # Execute deploy to grading pipeline inside student repository.
    return_code = _execute_deploy_to_grading(repo_path)
    success = (return_code == 0)

    # Return if D2G execution failed
    if not success:
        return success, repo_path, None

    # Collect overall points from result data
    results = _collect_results(repo_path)

    return success, repo_path, results

def _get_all_task_names(submission_results):
    # Get all tasknames by searching through all keys of the submission result.
    # If all submissions was correclty submitted, all should share the same
    # list of keys. Note: This is not tested here.
    keys = []
    for _, _, success, _, results in submission_results:
        # Only look for keys if we have data
        if success:
            for key in results[1].keys():
                if key not in keys:
                    keys.append(key)
    return keys


def _save_to_excel_file(submission_results):
    # Convert submission results to pandas dataframe and save them to an excel
    # file.

    # Create lists for temporarily storing the data.
    names, usernames, success_list, overall_points = [], [], [], []
    max_overall_points, submission_urls, repo_paths = [], [], []

    # We need to handle task points differently.
    task_names = _get_all_task_names(submission_results)
    task_points_list = [[] for _ in task_names]

    for _, submission, success, repo_path, results in submission_results:
        # Add name and username data by adding each individually
        names.extend(submission["Name"])
        usernames.extend(submission["Benutzername"])

        # Since this data holds information for multiple students, we need to
        # add it for each student.
        success_list.extend([success] * len(submission["Name"]))
        submission_urls.extend(
            [submission[URL_COLUMN]] * len(submission["Name"]))
        repo_paths.extend([repo_path] * len(submission["Name"]))

        # Only add actual points if data is available.
        if success:
            overall_points.extend([results[0][0]] * len(submission["Name"]))
            max_overall_points.extend(
                [results[0][1]] * len(submission["Name"]))

            # Handle task_points. The list holds information every task.
            for i, task_name in enumerate(task_names):
                task_points = results[1].get(task_name, (0, 0))
                task_points_list[i].extend(
                    [task_points] * len(submission["Name"]))
        else:
            # If no data is available, add zero as dummy points
            overall_points.extend([0] * len(submission["Name"]))
            # Since we don't know the actual max points here, we set it to
            # zero as well.
            max_overall_points.extend([0] * len(submission["Name"]))
            for i, task_name in enumerate(task_names):
                # And everything is zero here as well.
                task_points = (0, 0)
                task_points_list[i].extend(
                    [task_points] * len(submission["Name"]))

    # Create dataframe.
    df = pd.DataFrame({
        "Name": names,
        "Benutzername": usernames,
        "Erfolgreiche Bewertung": success_list,
        "Gesamtpunktzahl": overall_points,
        "Maximale Gesamtpunktzahl": max_overall_points,
        "Abgabe URLs": submission_urls,
        "Repositorypfad": repo_paths
    })

    # Add individual task points to the dataframe.
    for i, task_name in enumerate(task_names):
        df[f"Punktzahl {task_name}"] = \
            [point[0] for point in task_points_list[i]]
        df[f"Maximalpunktzahl {task_name}"] = \
            [point[1] for point in task_points_list[i]]

    # Sort dataframe so that it has the alphabetical order of the student.
    # This should make it easier to insert the results into ILIAS.
    df = df.sort_values(by="Name")
    df = df.reset_index(drop=True)
    # Save dataframe to excel file.
    df.to_excel(EXPORT_FILE)

def _check_for_plagiarism():
    # Executes the plagiarism metric scripts.

    # Execute plagiarism metric
    ret = subprocess.run([f"./scripts/metrics/{PLAGIARISM_METRIC}.sh"])
    
    # Only execute eval script if the metric execution was successful.
    if ret.returncode == 0:
        subprocess.run([f"./scripts/metrics/{PLAGIARISM_METRIC}_eval.py"])


def _main():
    # Read submission list from ILIAS file
    submissions = _read_submission_list()

    # Evaluate all submissions
    submission_results = []
    for id, submission in submissions.iterrows():
        success, repo_path, results = _evaluate_submission(submission)
        submission_results.append((id, submission, success, repo_path, results))

    _save_to_excel_file(submission_results)

    _check_for_plagiarism()

    print(f"Finished. Saved results to {EXPORT_FILE}.")

if __name__ == "__main__":

    _main()
