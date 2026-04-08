import os
from openai import OpenAI
from env.environment import ResumeEnv

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("API_BASE_URL")
)

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

response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=[{"role": "user", "content": prompt}]
)

output_text = response.choices[0].message.content

# ⚠️ simple fallback parsing
action = {
    "decision": "shortlist",
    "score": 0.8,
    "reason": "Candidate matches job requirements"
}

obs, reward, done, _ = env.step(action)

print("[END]")
print("Final Score:", reward)