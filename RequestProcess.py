import requests
import json
import os

url = "http://127.0.0.1:8000/process-data/"
headers = {"Content-Type": "application/json"}

data = {
    "pdf_path": "C:/Users/harin/Downloads/RagasOfCarnaticMusicByRamachandran_text.pdf",
    "json_paths": [
        "C:/Users/harin/Desktop/Carnatic/ragaData/ragas.json",
        "C:/Users/harin/Desktop/Carnatic/ragaData/swaras.json",
    ],
    "blog_url": "https://lyrical-thyagaraja.blogspot.com/",
}

# Check if files exist
for file_path in [data["pdf_path"]] + data["json_paths"]:
    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        exit(1)

try:
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)

    # Check if the request was successful
    response.raise_for_status()

    print("Response status code:", response.status_code)
    print("Response content:")
    print(response.text)

    # Try to parse JSON response
    try:
        json_response = response.json()
        print("Parsed JSON response:", json_response)
    except json.JSONDecodeError:
        print("Response is not in JSON format")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request: {e}")
    if hasattr(e, "response") and e.response is not None:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response content: {e.response.text}")
    else:
        print("No response received from the server")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
