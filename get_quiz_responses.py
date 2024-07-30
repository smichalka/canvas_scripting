import requests
import time
import csv
import os
from constants import CANVAS_API_TOKEN, CANVAS_API_URL, COURSE_ID

headers = {"Authorization": f"Bearer {CANVAS_API_TOKEN}"}


def get_quiz_objects(course_id):
    """
    Get a list of all the quizzes in a Canvas course

    Args:
        course_id: a string representing the Canvas course ID

    Returns:
        A list containing a list of Quiz objects, represented as dictionaries
    """

    url = f"{CANVAS_API_URL}/courses/{course_id}/quizzes"
    quizzes = []

    # Handle pagination so we can get all the quizzes
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        quizzes.extend(response.json())

        # Check for the 'next' link in the response headers
        links = response.headers.get("Link", "")
        next_link = None
        if links:
            for link in links.split(","):
                if 'rel="next"' in link:
                    next_link = link[link.find("<") + 1 : link.find(">")]
                    break

        url = next_link

    return quizzes


def get_homework_surveys_ids(quiz_objects):
    """
    Given a list of quiz objects, returns the homework surveys

    Args:
        quiz_objects: a list that contains Canvas Quiz objects, which are
        represented as dictionaries

    Returns:
        A dictionary of quiz IDs: quiz titles
    """
    homework_surveys = {}
    for quiz in quiz_objects:
        quiz_id = quiz["id"]
        quiz_name = quiz["title"]
        if "Homework" in quiz_name and "Survey" in quiz_name:
            homework_surveys[quiz_id] = quiz_name
    return homework_surveys


def get_homework_quizzes_ids(quiz_objects):
    """
    Given a list of quiz objects, returns the homework quizzes

    Args:
        quiz_objects: a list that contains Canvas Quiz objects, which are
        represented as dictionaries

    Returns:
        A dictionary of quiz IDs: quiz titles
    """
    homework_quizzes = {}
    for quiz in quiz_objects:
        quiz_id = quiz["id"]
        quiz_name = quiz["title"]
        if "Homework" in quiz_name and "Quiz" in quiz_name:
            homework_quizzes[quiz_id] = quiz_name
    return homework_quizzes


def create_quiz_report(course_id, quiz_id, report_type="student_analysis"):
    """
    Create a student analysis report on Canvas for a specific quiz

    Args:
        course_id: A string that represents the Canvas course ID
        quiz_id: A string that represents the Canvas quiz ID
        report_type: A string that represents the kind of report. Can be either 'student_analysis' or 'item_analysis'
    Returns:
        A dictionary of the raw data from the quiz report
    """
    url = f"{CANVAS_API_URL}/courses/{course_id}/quizzes/{quiz_id}/reports"
    payload = {"quiz_report[report_type]": report_type}
    response = requests.post(url, headers=headers, data=payload)
    return response.json()


def get_quiz_report_status(course_id, quiz_id, report_id):
    """
    Retrieve the quiz report and return it
    """
    url = f"{CANVAS_API_URL}/courses/{course_id}/quizzes/{quiz_id}/reports/{report_id}"
    response = requests.get(url, headers=headers)
    return response.json()


def download_report(file_url):
    """Download the quiz report"""
    response = requests.get(file_url, headers=headers)
    return response.content


def get_survey_csvs(quiz_objects):
    """
    Get homework survey student reports and download csv

    Args:
        quiz_objects - A list containing a list of Quiz objects, represented as dictionaries; returned by `get_quiz_objects`
    """
    surveys = get_homework_surveys_ids(quiz_objects)

    for quiz_id, title in surveys.items():
        assignment_num = [int(s) for s in title.split() if s.isdigit()][0]
        quiz_file_path = f"Homework {assignment_num} Quiz.csv"
        if os.path.exists(quiz_file_path) and os.path.isfile(quiz_file_path):
            report = create_quiz_report(COURSE_ID, quiz_id)
            time.sleep(1)
            report_id = report["id"]

            # Poll until the report is complete
            while True:
                report_status = get_quiz_report_status(COURSE_ID, quiz_id, report_id)
                if "file" in report_status:
                    if report_status["file"]["upload_status"] == "success":
                        file_url = report_status["file"]["url"]
                        break
                time.sleep(5)  # wait before polling again

            # Download the report
            report_content = download_report(file_url)
            time.sleep(1)

            # Save the report to a file
            report_file = f"{title}.csv"
            with open(report_file, "wb") as file:
                file.write(report_content)
            time.sleep(1)


def get_quiz_csvs(course_id, quiz_id, csv_file):
    ###### Might require pagination handling? Need more students to be sure ###########
    ###### See `get_quiz_objects` for pagination implementation
    """
    Use requests to get student grades on a specific assignment
    If there are no grades/responses to a quiz it will not create a csv

    Args:
        course_id: String that represents the Canvas course ID
        quiz_id: String that represents the Canvas quiz ID
    """
    grades_url = f"{CANVAS_API_URL}/courses/{course_id}/quizzes/{quiz_id}/submissions"
    response = requests.get(grades_url, headers=headers)

    if response.status_code == 200:
        grades = response.json()
        grades = grades["quiz_submissions"]
    else:
        print(f"Failed to fetch grades: {response.status_code}")
        grades = None

    # Check if grades were fetched successfully
    if grades:

        # Open the CSV file for writing
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write the header
            writer.writerow(["id", "Quiz Grade"])

            # Write the grades
            for grade in grades:
                student_id = grade["user_id"]
                score = grade["score"]
                total_points = grade["quiz_points_possible"]
                grade_value = round(score / total_points, 2) * 100
                writer.writerow([student_id, grade_value])


def main():
    """Main method"""
    all_quizzes = get_quiz_objects(COURSE_ID)
    quiz_ids = get_homework_quizzes_ids(all_quizzes)
    for quiz_id, title in quiz_ids.items():
        csv_name = f"{title}.csv"
        get_quiz_csvs(COURSE_ID, quiz_id, csv_name)
        time.sleep(1)
    get_survey_csvs(all_quizzes)


if __name__ == "__main__":
    main()
