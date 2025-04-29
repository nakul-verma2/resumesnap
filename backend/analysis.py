import requests
from dotenv import load_dotenv
import os
import re
import ast


load_dotenv()


def markdown_bold_to_html(text):
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)


def resume_weakness(resume_text, job_description=None):
    print("🔍 Finding weakness in resume... Please wait.")
    api_key = os.getenv('ANALYSIS_API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "Imagine you are a resume analysis expert. Analyze the below resume text "
        "and job title (if provided) and tell about the weakness only in it according "
        "to job role desired 'WITHOUT ANY MARKDOWN ONLY using bullets'."
    )

    user_prompt = f"Job description:\n{job_description.strip()}\nResume:\n{resume_text.strip()}" if job_description else f"Resume:\n{resume_text.strip()}"

    data = {
        'model': 'mistralai/mistral-7b-instruct:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        raw_output = response.json()['choices'][0]['message']['content']
        result = markdown_bold_to_html(raw_output)
        print("✅ Analysis complete!")
        return result
    else:
        print("❌ Error during resume analysis.")
        return f"Error: {response.status_code} - {response.text}"


def resume_improve(resume_text, job_description=None):
    print("🔍 Marking the need of improvement... Please wait.")
    api_key = os.getenv('ANALYSIS_API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "Imagine you are a resume analysis expert. Analyze the below resume text "
        "and tell about the areas of improvement and new skills to learn only according "
        "to job role desired 'WITHOUT ANY MARKDOWN' in 250 words."
    )

    user_prompt = f"Job description:\n{job_description.strip()}\nResume:\n{resume_text.strip()}" if job_description else f"Resume:\n{resume_text.strip()}"

    data = {
        'model': 'mistralai/mistral-7b-instruct:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        raw_output = response.json()['choices'][0]['message']['content']
        result = markdown_bold_to_html(raw_output)
        print("✅ Analysis complete!")
        return result
    else:
        print("❌ Error during resume analysis.")
        return f"Error: {response.status_code} - {response.text}"


def scoring(resume_text):
    print("🔍 Calculating scores of resume... Please wait.")
    api_key = os.getenv('SCORE_API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "Analyze the following resume text and return a Python dictionary with a score out of 10 for each of the following labels: "
        "content, ats_friendly, skills, workexpirence. Do not include any comments or explanations."
    )

    user_prompt = f"Resume:\n{resume_text.strip()}"

    data = {
        'model': 'google/gemma-3-27b-it:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        cleaned = content.replace("```python", "").replace("```", "").strip()
        try:
            result_dict = ast.literal_eval(cleaned)
            print("✅ Analysis complete!")
            return result_dict
        except (ValueError, SyntaxError):
            print("⚠️ Failed to convert response to dictionary.")
            return {"error": "Invalid format in response"}
    else:
        print("❌ Error during resume analysis.")
        return {"error": f"{response.status_code} - {response.text}"}


def score(resume_text):
    print("🔍 Calculating overall score of resume... Please wait.")
    api_key = os.getenv('SCORE_API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = "Analyze the following resume text and return a number of a score out of 100 only nothing else."
    user_prompt = f"Resume:\n{resume_text.strip()}"

    data = {
        'model': 'google/gemma-3-27b-it:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content'].strip()
        print("✅ Analysis complete!")
        return result
    else:
        print("❌ Error during resume analysis.")
        return f"Error: {response.status_code} - {response.text}"


