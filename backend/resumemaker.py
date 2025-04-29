import requests
from dotenv import load_dotenv
import os
import ast

load_dotenv()

def generate_resume(name, email, phone, summary):
    print("💡 Generating resume via AI...")

    api_key = os.getenv('MAKER_KEY')
    url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    system_prompt = (
        "You are a professional resume writer. Given some user information, generate a clean, ATS-Optimezed resume. "
        "Convert the short provided details into more detailed sections, ensuring each work experience entry includes a job title, duration (e.g., '2 years'), and specific achievements or responsibilities. "
        "For projects, provide a brief description or key features based on the project names if details are not provided. "
        "Return the resume ONLY as a valid Python dictionary using the following format (include only provided fields):\n\n"
        "{\n"
        "  'name': str,\n"
        "  'email': str,\n"
        "  'phone': str,\n"
        "  'summary': str,\n"
        "  'skills': list[str],\n"
        "  'work_experience': list[str],\n"
        "  'education': list[str],\n"
        "  'projects': list[str]\n"
        "}\n\n"
        "For Projects, return in this specific format like project name: project description. Do not use anything else other than ':' as the separator. "
        "For summary, create a concise professional summary (2-3 sentences) based on the provided text, highlighting experience, skills, and passion. "
        "If any section is not provided, omit it from the dictionary. DO NOT return anything else, just the dictionary."
    )

    user_prompt = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Summary: {summary}\n"
        f"Generate a professional resume based on this."
    )

    data = {
        'model': 'google/gemma-3-27b-it:free',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("✅ Resume generated successfully!")
        content = response.json()['choices'][0]['message']['content']
        cleaned = content.replace("```python", "").replace("```", "").strip()
        try:
            parsed_resume = ast.literal_eval(cleaned)
            return parsed_resume
        except Exception as e:
            print("⚠️ Failed to parse response into dictionary:", e)
            return cleaned
    else:
        print("❌ Failed to generate resume.")
        return f"Error: {response.status_code} - {response.text}"


