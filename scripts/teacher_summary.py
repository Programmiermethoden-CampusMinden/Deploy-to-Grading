#!/bin/python3

import pandas as pd
import sys

EXPORT_FILE = "semester_results.xlsx"
USAGE = """usage: teacher_summary.py [submission_files...]
       Create a summary of the submissions of all assignments.

       Params:
       submission_files List of paths to all submission result files created
                        by the deploy_to_grading_teacher.py script.
"""

def _print_error_and_exit(error_msg):
    print(error_msg)
    print(USAGE)
    exit(-1)

def _load_submission_results():
    # Load the submission results from the excel files.
    dataframes = []
    # Submission files are listed in sys.argv
    for path in sys.argv[1:]:
        try:
            dataframes.append(pd.read_excel(path))
        except:
            _print_error_and_exit(f"Failed to read submission result {path}.")

    # Exit if no dataframes were loaded.
    if len(dataframes) == 0:
        _print_error_and_exit(f"No submission results were loaded.")

    return dataframes

def _prepare_dataframes(result_dfs):
    # Prepares the dataframe so that it can be combined with the other#
    # dataframes.
    new_dfs= []
    for i, df in enumerate(result_dfs):
        new_df = df[["Benutzername", "Name"]].copy(deep=True)
        # We need to rename the columns here to avoid name conflicts.
        new_df[f"Punkte Aufgabenblatt {i+1}"] = df["Gesamtpunktzahl"]
        new_df[f"Maximale Punkte Aufgabenblatt {i+1}"] = \
            df["Maximale Gesamtpunktzahl"]
        new_dfs.append(new_df)

    return new_dfs

def _merge_dataframes(result_dfs):
    # Creates a single dataframe with all the necessary data.

    # Prepare the individual dataframes for merging.
    prepared_dfs = _prepare_dataframes(result_dfs)
    # Merged dataframes
    merged_df = pd.concat(prepared_dfs, ignore_index=True)
    # Group the dataframe by username so that we have all points of a user in
    # a single row.
    grouped_df = merged_df.groupby("Benutzername").agg("max")
    # Fill all NaN values with zero. Students have NaN as a value when they are
    # not listed in the result file of a given submission.
    filled_df = grouped_df.fillna(0)

    return filled_df

def _calcualte_overall_points(merged_df, assignment_count):
    # Sums up the points of all the individual assignments.

    # Create initial dataframe and copy all data.
    final_df = merged_df.copy(deep=True)
    final_df["Gesamtpunktzahl"] = 0
    final_df["Maximale Gesamtpunktzahl"] = 0

    # Sum up the points of all assignments.
    for i in range(assignment_count):
        final_df["Gesamtpunktzahl"] += merged_df[f"Punkte Aufgabenblatt {i+1}"]
        final_df["Maximale Gesamtpunktzahl"] += \
            merged_df[f"Maximale Punkte Aufgabenblatt {i+1}"]

    return final_df

def _save_to_excel_file(final_df):
    # Formats and saves dataframe to excel file.

    # Determine new column ordering. We want to have the overall points
    # before the individual assignment points.
    columns = final_df.columns.values
    new_columns = []
    new_columns.extend(columns[0:1])
    new_columns.extend(["Gesamtpunktzahl", "Maximale Gesamtpunktzahl"])
    new_columns.extend(columns[1:-2])

    # Reorder and sort by student name in alphabetical order. The ordering
    # should make it easier to transfer the results back into ILIAS.
    final_df = final_df[new_columns]
    final_df = final_df.sort_values(by="Name")

    # Save dataframe to excel file.
    final_df.to_excel(EXPORT_FILE)

def _main():
    # Load all submission result files.
    result_dfs = _load_submission_results()

    # Bring all data into usable format.
    merged_df = _merge_dataframes(result_dfs)
    final_df = _calcualte_overall_points(merged_df, len(result_dfs))

    # Save data to disc.
    _save_to_excel_file(final_df)

if __name__ == "__main__":
    _main()
