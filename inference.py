import os
import requests
import json
from dotenv import load_dotenv
from env.environment import ResumeEnv

load_dotenv()

API_KEY = os.getenv("AIzaSyBf14w9-7E3DdEiNyfirDITArSWgPZMEyo")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

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

Strictly return ONLY valid JSON:
{{
  "decision": "shortlist or reject",
  "score": 0 to 1,
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

# 🧠 Extract text
try:
    output_text = result["candidates"][0]["content"]["parts"][0]["text"]
except:
    output_text = ""

print("AI RAW OUTPUT:", output_text)

# 🔥 JSON PARSING
try:
    # clean text (remove ```json if present)
    cleaned = output_text.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)

    action = {
        "decision": parsed.get("decision", "reject"),
        "score": float(parsed.get("score", 0)),
        "reason": parsed.get("reason", "")
    }

except Exception as e:
    print("Parsing failed, using fallback:", e)

    action = {
        "decision": "reject",
        "score": 0.5,
        "reason": "Parsing failed fallback"
    }

# ✅ STEP with REAL action
obs, reward, done, _ = env.step(action)

print("[END]")
print("Final Score:", reward)