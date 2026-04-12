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

# Toggle mode based on API key
USE_REAL_API = bool(OPENAI_API_KEY)

print("Mode:", "REAL API" if USE_REAL_API else "MOCK")

# -------------------------
# Init OpenAI Client (only if key exists)
# -------------------------
if USE_REAL_API:
    client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------
# LLM Call Function (REAL + MOCK)
# -------------------------
def call_llm(prompt):
    if USE_REAL_API:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content

    else:
        print("[MOCK MODE ENABLED]")

        # Simulated realistic response
        return json.dumps({
            "decision": "shortlist",
            "score": 0.78,
            "reason": "Candidate has relevant skills and experience matching the job description."
        })

# -------------------------
# Init Environment
# -------------------------
env = ResumeEnv()

print("[START]")

obs = env.reset()

print("[STEP]")
print("Job:", obs.job_description)
print("Resume:", obs.resume)

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
# Call LLM (REAL or MOCK)
# -------------------------
raw_output = call_llm(prompt)

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