import time
import requests
import os
from dotenv import load_dotenv
import json
import ast

load_dotenv()



def extract_info_from_text(resume_text):
    print("🔍 Analyzing resume... Please wait.")

    api_key = os.getenv('DETAILS_API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "You are an expert resume parser. Extract the following fields from the resume: "
        "Name, Email, Phone Number, and Skills. Return the result ONLY as a Python dictionary, "
        "without any extra explanation or markdown formatting. If a field is missing, use 'none'."
    )

    data = {
        'model': 'mistralai/mistral-7b-instruct:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': resume_text}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        resp_json = response.json()
    except ValueError:
        print("❌ Invalid JSON response.")
        return f"Error: {response.status_code} - {response.text}"

    if response.status_code == 200 and 'choices' in resp_json:
        print("✅ Basic data extraction complete!")
        return resp_json['choices'][0]['message']['content']
    else:
        print("❌ Unexpected error.")
        return f"Error: {response.status_code} - {response.text}"


def education(resume_text):
    print("💼 Extracting Education Details... Please wait.")

    api_key = os.getenv('DETAILS_API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "Extract the significant education detail from resume below like degrees from the following text "
        "into a single line separated by commas and nothing else."
    )

    data = {
        'model': 'mistralai/mistral-7b-instruct:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': resume_text}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        resp_json = response.json()
    except ValueError:
        print("❌ Invalid JSON response.")
        return f"Error: {response.status_code} - {response.text}"

    if response.status_code == 200 and 'choices' in resp_json:
        print("✅ Education extraction complete!")
        return resp_json['choices'][0]['message']['content']
    else:
        print("❌ Unexpected error.")
        return f"Error: {response.status_code} - {response.text}"


def workexperience(resume_text):
    print("💼 Extracting work experience... Please wait.")

    api_key = os.getenv('DETAILS_API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "Extract work experience from the following resume into a single comma-separated line without any "
        "labels or extra text. Return only plain text limited to 150 words."
    )

    data = {
        'model': 'mistralai/mistral-7b-instruct:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': resume_text}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        resp_json = response.json()
    except ValueError:
        print("❌ Invalid JSON response.")
        return f"Error: {response.status_code} - {response.text}"

    if response.status_code == 200 and 'choices' in resp_json:
        print("✅ Work experience extraction complete!")
        return resp_json['choices'][0]['message']['content']
    else:
        print("❌ Unexpected error.")
        return f"Error: {response.status_code} - {response.text}"


def extract_resume_details(resume_text: str) -> dict:
    result_str = extract_info_from_text(resume_text)
    try:
        result = ast.literal_eval(result_str)
    except Exception as e:
        print(f"❌ Failed to parse dictionary: {e}")
        result = {}

    time.sleep(1)
    result["Education"] = education(resume_text)
    time.sleep(1)
    result["Work Experience"] = workexperience(resume_text)
    time.sleep(1)

    print("✅ Resume parsing complete! 🎉\n")
    return result
