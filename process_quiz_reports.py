import pandas as pd


def process_reports(quiz_csv, survey_csv, combined_csv):
    """
    Consolidate survey and quiz reports into one csv, remove unimportant information

    Args:
        quiz_csv: string that represents the file path to a quiz report csv
        survey_csv: string that represents the file path to a survey report csv
        combined_csv: string that represents the name of the consolidated report

        ^^^ All strings must end with .csv
    """
    quiz = pd.read_csv(quiz_csv)
    survey = pd.read_csv(survey_csv)
    dropped_columns = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 17, 18, 19]
    survey = survey.drop(survey.columns[dropped_columns], axis=1)

    merged_df = pd.merge(survey, quiz, on="id", how="inner")
    merged_df.to_csv(combined_csv, index=False)
    print("Reports Processed")


process_reports("Homework 6 Quiz.csv", "Homework 6 Survey.csv", "modified_csv.csv")
