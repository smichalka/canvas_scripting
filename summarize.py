from secret_constants import AZURE_TOKEN, AZURE_ENDPOINT
import requests


def getGPTResponses():
    # Configuration
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_TOKEN,
    }

    deployment_name = "QEA_Processing"
    api_version = "2024-05-13"

    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Tell me key events of the French Revolution.",
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 4000,
    }

    url = f"{AZURE_ENDPOINT}/openai/deployments/{deployment_name}/completions?api-version={api_version}"
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")


response = getGPTResponses()
print(response)
