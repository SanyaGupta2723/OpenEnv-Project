from pydantic import BaseModel

class Observation(BaseModel):
    job_description: str
    resume: str

class Action(BaseModel):
    decision: str   # shortlist / reject
    score: float    # 0–1
    reason: str

class Reward(BaseModel):
    score: float