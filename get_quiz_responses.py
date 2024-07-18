import requests
import time
from secret_constants import API_TOKEN, API_URL, COURSE_ID

QUIZ_ID = "2192"  # HW1 Survey
headers = {"Authorization": f"Bearer {API_TOKEN}"}


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


def main():
    """Main method"""
    report_file = "quiz_report.csv"
    report = create_quiz_report(COURSE_ID, QUIZ_ID)
    report_id = report["id"]

    # Poll until the report is complete
    while True:
        report_status = get_quiz_report_status(COURSE_ID, QUIZ_ID, report_id)
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


if __name__ == "__main__":
    main()
