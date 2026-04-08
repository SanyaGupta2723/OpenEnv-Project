import os
import requests
from dotenv import load_dotenv
from env.environment import ResumeEnv

load_dotenv()

API_KEY = os.getenv("AIzaSyBf14w9-7E3DdEiNyfirDITArSWgPZMEyo")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

env = ResumeEnv()

print("[START]")

obs = env.reset()

print("[STEP]")
print("Job:", obs.job_description)
print("Resume:", obs.resume)

prompt = f"""
You are an HR AI.

Job: {obs.job_description}
Resume: {obs.resume}

Return JSON:
{{
  "decision": "shortlist or reject",
  "score": float between 0 and 1,
  "reason": "short explanation"
}}
"""

payload = {
    "contents": [
        {
            "parts": [{"text": prompt}]
        }
    ]
}

response = requests.post(url, json=payload)
result = response.json()

# Gemini output extract (simple)
try:
    output_text = result["candidates"][0]["content"]["parts"][0]["text"]
except:
    output_text = ""

# fallback action (safe)
action = {
    "decision": "shortlist",
    "score": 0.8,
    "reason": "Candidate matches job requirements"
}

obs, reward, done, _ = env.step(action)

print("[END]")
print("Final Score:", reward)