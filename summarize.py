from constants import (
    AZURE_TOKEN,
    AZURE_ENDPOINT,
    GPT_OUTPUT_CSV,
    AZURE_DEPLOYMENT_NAME,
    AZURE_API_VERSION,
)
import requests
import csv
import pandas as pd  # pylint: disable=import-error
import os
import time

headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_TOKEN,
}

deployment_name = AZURE_DEPLOYMENT_NAME
api_version = AZURE_API_VERSION


def get_summary(assignment_responses):
    """
    Create a GPT-generated summary of where students struggled based on survey responses

    Args:
        assignment_responses: a txt file that has all student responses responses saved for a specific assignment

    Returns:
        gtp_output: A string that contains that summary gpt generated
    """
    # Open the file in read mode ('r') and read its contents
    with open("prompt.txt", "r") as file:
        prompt = file.read()

    with open(assignment_responses, "r") as file:
        survey_content = file.read()

    gpt_input = prompt + survey_content

    # Payload for the request
    payload = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": gpt_input}]}
        ],
        "temperature": 0.7,
        "max_tokens": 3000,
    }

    url = f"{AZURE_ENDPOINT}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}-preview"
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response = response.json()
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    result = response["choices"][0]
    gtp_output = result["message"]["content"]
    return gtp_output


def initialize_csv(csv_name):
    """
    Create a csv to save summaries to with assignment name

    Args:
        csv_name: A string that is the name of the csv being created
    """
    with open(csv_name, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Assignment", "Summary"])


def store_response(csv_name, survey_responses):
    """
    Save GPT-generated summaries to csv with corresponding assignment name

    Args:
        survey_responses: a txt file that has all survey responses for an assignment saved
        csv_name: The name of the csv the summaries are being saved to
    """
    gpt_output = get_summary(survey_responses)
    assignment_name = survey_responses[:-4]
    summaries = pd.read_csv(csv_name)
    summaries.loc[len(summaries)] = [assignment_name, gpt_output]

    summaries.to_csv(csv_name, index=False)


def main():
    """Go through all assignment txt files and add summary to GPT_OUTPUT_CSV"""
    initialize_csv(GPT_OUTPUT_CSV)
    for filename in os.listdir("."):
        if (
            filename.endswith(".txt")
            and filename != "requirements.txt"
            and filename != "prompt.txt"
        ):
            store_response(GPT_OUTPUT_CSV, filename)
            os.remove(filename)
            time.sleep(1)


if __name__ == "__main__":
    main()
