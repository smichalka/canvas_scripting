import requests
import time
import csv
from secret_constants import API_TOKEN, API_URL, COURSE_ID

headers = {"Authorization": f"Bearer {API_TOKEN}"}


def get_quiz_objects(course_id):
    """
    Get a list of all the quizzes in a Canvas course

    Args:
        course_id: a string representing the Canvas course ID

    Returns:
        A list containing a list of Quiz objects, represented as dictionaries
    """

    url = f"{API_URL}/courses/{course_id}/quizzes"
    quizzes = []

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
        # print(quiz_name)
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
    url = f"{API_URL}/courses/{course_id}/quizzes/{quiz_id}/reports"
    payload = {"quiz_report[report_type]": report_type}
    response = requests.post(url, headers=headers, data=payload)
    return response.json()


def get_quiz_report_status(course_id, quiz_id, report_id):
    """
    Retrieve the quiz report and return it
    """
    url = f"{API_URL}/courses/{course_id}/quizzes/{quiz_id}/reports/{report_id}"
    response = requests.get(url, headers=headers)
    return response.json()


def download_report(file_url):
    """Download the quiz report"""
    response = requests.get(file_url, headers=headers)
    return response.content


def get_survey_csvs(quiz_objects):
    """Get homework survey student reports and download csv"""
    surveys = get_homework_surveys_ids(quiz_objects)
    consolidated_data = []
    headers = None

    for quiz_id, title in surveys.items():
        # report_file = f"{title}.csv"
        report = create_quiz_report(COURSE_ID, quiz_id)
        time.sleep(1)
        report_id = report["id"]

        # Poll until the report is complete
        while True:
            report_status = get_quiz_report_status(COURSE_ID, quiz_id, report_id)
            # print(report_status)
            if "file" in report_status:
                if report_status["file"]["upload_status"] == "success":
                    file_url = report_status["file"]["url"]
                    break
            time.sleep(5)  # wait before polling again

        # Download the report
        report_content = download_report(file_url)
        time.sleep(1)

        # Read the report content and add it to the consolidated data
        report_lines = report_content.decode("utf-8").splitlines()
        report_reader = csv.reader(report_lines)
        report_data = list(report_reader)

        if headers is None:
            headers = report_data[0] + ["Survey Title"]
            consolidated_data.append(headers)

        for row in report_data[1:]:
            row.append(title)
            consolidated_data.append(row)

        print(f"Report processed: {title}")

    with open("consolidated_survey_reports.csv", "w", newline="") as consolidated_file:
        writer = csv.writer(consolidated_file)
        writer.writerows(consolidated_data)
    print("Consolidated report generated: consolidated_survey_reports.csv")

    # # Save the report to a file
    # with open(report_file, "wb") as file:
    #     file.write(report_content)
    # print(f"Report generated: {report_file}")
    # time.sleep(1)


def get_quiz_csvs(quiz_objects):
    """Get homework quiz student reports and download csv"""

    quizzes = get_homework_quizzes_ids(quiz_objects)
    for quiz_id, title in quizzes.items():
        report_file = f"{title}.csv"
        report = create_quiz_report(COURSE_ID, quiz_id)
        time.sleep(1)
        report_id = report["id"]

        # Poll until the report is complete
        while True:
            report_status = get_quiz_report_status(COURSE_ID, quiz_id, report_id)
            # print(report_status)
            if "file" in report_status:
                if report_status["file"]["upload_status"] == "success":
                    file_url = report_status["file"]["url"]
                    break
            time.sleep(5)  # wait before polling again

        # Download the report
        report_content = download_report(file_url)

        # Save the report to a file
        with open(report_file, "wb") as file:
            file.write(report_content)
        print(f"Report generated: {report_file}")
        time.sleep(1)


def main():
    """Main method"""
    all_quizzes = get_quiz_objects(COURSE_ID)
    get_survey_csvs(all_quizzes)
    # get_quiz_csvs(all_quizzes)


if __name__ == "__main__":
    main()
