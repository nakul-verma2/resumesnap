import requests
import os
from dotenv import load_dotenv

load_dotenv()


def summary(resume_text):
    print("🔍 Making summary of resume... Please wait.")

    api_key = os.getenv('API_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "Extract summary or overview section from the following resume text. Return only the summary content and nothing else."
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

    if 'error' in resp_json:
        error_msg = resp_json['error']['message']
        print(f"❌ API Error: {error_msg}")
        return f"API Error: {error_msg}"
    
    if response.status_code == 200 and 'choices' in resp_json:
        print("✅ Summary generation complete!")
        reply = response.json()['choices'][0]['message']['content']
        return reply.strip()
    else:
        print("❌ Unexpected error.")
        return f"Error: {response.status_code} - {response.text}"
