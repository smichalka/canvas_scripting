import requests
import csv
import time
from secret_constants import API_TOKEN, API_URL, COURSE_ID

QUIZ_ID = "2192"  # HW1 Survey
time_delay = 1

# Headers for authentication
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# Function to get quiz submissions for a specific quiz
def get_quiz_submissions(course_id, quiz_id):
    submissions_url = f"{API_URL}/courses/{course_id}/quizzes/{quiz_id}/submissions"
    response = requests.get(submissions_url, headers=headers)

    if response.status_code == 200:
        return response.json()["quiz_submissions"]
    else:
        print(f"Failed to fetch quiz submissions: {response.status_code}")
        # print(response.json())  # Print the error response for debugging
        return None


# Function to get the details of the answers given in a submission
def get_submission_answers(course_id, quiz_id, submission_id):
    # answers_url = (
    #     f"{API_URL}/courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}"
    # )
    answers_url = f"{API_URL}/courses/{course_id}/quizzes/{quiz_id}/submissions?include[]=submission_history"
    # print(answers_url)
    response = requests.get(answers_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Failed to fetch answers for submission_id {submission_id}: {response.status_code}"
        )
        # print(response.json())  # Print the error response for debugging
        return None


# Fetch quiz submissions
submissions = get_quiz_submissions(COURSE_ID, QUIZ_ID)

if submissions:
    for submission in submissions:
        submission_id = submission["submission_id"]
        temp_id = submission["id"]
        student_id = submission["user_id"]
        # print("NEW SUBMISSION")
        # print(submission_id)
        # print(temp_id)
        # print(student_id)
        print("ATTEMPT")
        answers = get_submission_answers(COURSE_ID, QUIZ_ID, temp_id)
        print(answers)
        # quiz_submissions = answers["quiz_submissions"]
        # # print(quiz_submissions)
        # for result in quiz_submissions:
        #     for key, value in result.items():
        #         print(f"{key}:{value}\n")


# {'quiz_submissions': [{'id': 44222, 'quiz_id': 2192, 'quiz_version': 3, 'user_id': 1041, 'submission_id': 429506, 'score': 0.0, 'kept_score': 0.0, 'started_at': '2024-07-16T20:25:43Z', 'end_at': None, 'finished_at': '2024-07-16T20:29:17Z', 'attempt': 1, 'workflow_state': 'pending_review', 'fudge_points': None, 'quiz_points_possible': 3.0, 'extra_attempts': None, 'extra_time': None, 'manually_unlocked': None, 'validation_token': '3925eec2b6c8057b29e0533ca43bd53e24ca46920683f9bb3ead26227628eb29', 'score_before_regrade': None, 'has_seen_results': False, 'time_spent': 213, 'attempts_left': 0, 'overdue_and_needs_submission': False, 'excused?': False, 'html_url': 'https://canvas.olin.edu/courses/790/quizzes/2192/submissions/44222', 'result_url': 'https://canvas.olin.edu/courses/790/quizzes/2192/history?quiz_submission_id=44222&version=1'}]}


# # Check if submissions were fetched successfully
# if submissions:
#     # Specify the CSV file name
#     csv_file = "quiz_answers.csv"

#     # Open the CSV file for writing
#     with open(csv_file, mode="w", newline="") as file:
#         writer = csv.writer(file)

#         # Write the header
#         writer.writerow(
#             [
#                 "Student ID",
#                 "Submission ID",
#                 "Question ID",
#                 "Question Text",
#                 "Student Answer",
#             ]
#         )

#         # Write the answers
#         for submission in submissions:
#             # print(submission)
#             student_id = submission["user_id"]
#             submission_id = submission["id"]
#             answers = get_submission_answers(COURSE_ID, QUIZ_ID, submission_id)

#             if answers:
#                 print("Found Submission")
#                 for answer in answers["quiz_submission_questions"]:
#                     question_id = answer["id"]
#                     question_text = answer["question_text"]
#                     student_answer = answer["answer"]
#                     writer.writerow(
#                         [
#                             student_id,
#                             submission_id,
#                             question_id,
#                             question_text,
#                             student_answer,
#                         ]
#                     )
#                     time.sleep(time_delay)  # To avoid hitting rate limits
#             else:
#                 print("No submission")

#     print(f"Quiz answers have been written to {csv_file}")
# else:
#     print("No submissions to write.")
