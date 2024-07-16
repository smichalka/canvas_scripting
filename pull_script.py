import requests
import csv
import time
from secret_constants import API_TOKEN, API_URL, COURSE_ID

ASSIGNMENT_ID = "2193"  # HW1 Quiz
time_delay = 0.25

# Headers for authentication
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# Function to get grades for a specific assignment
def get_assignment_grades(course_id, assignment_id):
    """
    Use requests to get student grades on a specific assignment

    Args:
        course_id: String that represents the Canvas course ID
        assignment_id: String that represents the Canvas assignment ID
    """
    grades_url = (
        f"{API_URL}/courses/{course_id}/assignments/{assignment_id}/submissions"
    )
    response = requests.get(grades_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch grades: {response.status_code}")
        return None


# Function to get user details by user_id
def get_user_details(user_id):
    """
    Use requests to get the student name that matches a student ID

    Args:
        user_id: String that represents a student's ID on Canvas
    """
    user_url = f"{API_URL}/users/{user_id}/profile"
    response = requests.get(user_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Failed to fetch user details for user_id {user_id}: {response.status_code}"
        )
        return None


# Fetch grades
grades = get_assignment_grades(COURSE_ID, ASSIGNMENT_ID)

# Check if grades were fetched successfully
if grades:
    # Specify the CSV file name
    csv_file = "grades.csv"

    # Open the CSV file for writing
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Student ID", "Student Name", "Grade", "Submitted At"])

        # Write the grades
        for grade in grades:
            student_id = grade["user_id"]
            # user_details = get_user_details(student_id)
            # student_name = user_details["name"] if user_details else "N/A"
            student_name = "N/A"
            grade_value = grade["grade"]
            submitted_at = grade["submitted_at"]
            writer.writerow([student_id, student_name, grade_value, submitted_at])
            # time.sleep(time_delay)  # To avoid hitting rate limits

    print(f"Grades have been written to {csv_file}")
else:
    print("No grades to write.")
