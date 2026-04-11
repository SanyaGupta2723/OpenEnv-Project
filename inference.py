import os
import requests
import json
from dotenv import load_dotenv
from env.environment import ResumeEnv

# 🔑 Load env variables
load_dotenv()

API_KEY = os.getenv("YOUR_API_KEY")

# ❗ Check if API key loaded
if not API_KEY:
    raise ValueError("YOUR_API_KEY not found. Check your .env file")

# 🌐 Gemini API URL
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
env = ResumeEnv()

print("[START]")

obs = env.reset()

print("[STEP]")
print("Job:", obs.job_description)
print("Resume:", obs.resume)

# 🧾 Prompt
prompt = f"""
You are an HR AI.

Job: {obs.job_description}
Resume: {obs.resume}

Strictly return ONLY valid JSON (no extra text):
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

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

print("FULL API RESPONSE:", result)

# 🧠 Extract AI text safely
output_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

print("AI RAW OUTPUT:", output_text)

# 🔥 JSON Parsing
try:
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
        "reason": "Fallback due to parsing error"
    }

# ✅ Environment step
obs, reward, done, _ = env.step(action)

print("[END]")
print("Final Score:", reward)