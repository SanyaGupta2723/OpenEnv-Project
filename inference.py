# inference.py

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from env.environment import ResumeEnv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Add it in your .env file.")

# -------------------------
# Init OpenAI Client
# -------------------------
client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------
# Init Environment
# -------------------------
env = ResumeEnv()

print("[START]")

obs = env.reset()

print("[STEP]")
print("Job:", obs.job_description)
print("Resume:", obs.resume)
print("Loaded Key:", os.getenv("OPENAI_API_KEY"))

# -------------------------
# Prompt
# -------------------------
prompt = f"""
You are an HR AI.

Job Description:
{obs.job_description}

Resume:
{obs.resume}

Return ONLY valid JSON in this format:
{{
  "decision": "shortlist or reject",
  "score": 0 to 1,
  "reason": "short explanation"
}}
"""

# -------------------------
# Call OpenAI
# -------------------------
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0
)

raw_output = response.choices[0].message.content

print("AI RAW OUTPUT:", raw_output)

# -------------------------
# Parse JSON safely
# -------------------------
try:
    cleaned = raw_output.replace("```json", "").replace("```", "").strip()
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

# -------------------------
# Environment Step
# -------------------------
obs, reward, done, _ = env.step(action)

print("[END]")
print("Final Score:", reward)