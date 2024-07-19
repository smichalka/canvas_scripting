import requests
import csv
import time
from secret_constants import API_TOKEN, API_URL, COURSE_ID

ASSIGNMENT_ID = "2211"  # HW6 Quiz
time_delay = 0.25

# Headers for authentication
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def create_student_csv(course_id, csv_file):
    """
    Use Canvas API to get a list of users, save user names and IDs to a csv

    Args:
        course_id: A string representing the Canvas course id
        csv_file: A string representing the name of the file data is being saved to
            Must end with .csv
    """
    url = f"{API_URL}/courses/{course_id}/users"
    users = []

    # Handle pagination and get all students
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        users.extend(response.json())

        # Check for the 'next' link in the response headers
        links = response.headers.get("Link", "")
        next_link = None
        if links:
            for link in links.split(","):
                if 'rel="next"' in link:
                    next_link = link[link.find("<") + 1 : link.find(">")]
                    break
        url = next_link

    # Write users to csv file
    if users:
        # Open the CSV file for writing
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["id", "name"])
            for user in users:
                student_id = user["id"]
                student_name = user["name"]
                writer.writerow([student_id, student_name])
        print(f"Student List Created: {csv_file}")
    else:
        print("No students to list")


create_student_csv(COURSE_ID, "students.csv")
