import random
from .models import Observation

class ResumeEnv:

    def __init__(self):
        self.data = [
            {
                "job": "Python Developer with ML",
                "resume": "3 years Python, ML projects, NLP experience",
                "correct": {"decision": "shortlist", "score": 0.9}
            },
            {
                "job": "Frontend Developer",
                "resume": "Only HTML CSS basic JS",
                "correct": {"decision": "reject", "score": 0.3}
            },
            {
                "job": "Data Scientist",
                "resume": "Statistics + Python + ML + Deep Learning",
                "correct": {"decision": "shortlist", "score": 0.95}
            }
        ]
        self.current = None

    def reset(self):
        self.current = random.choice(self.data)
        return Observation(
            job_description=self.current["job"],
            resume=self.current["resume"]
        )

    def step(self, action):
        correct = self.current["correct"]

        score = 0.0

        # Decision match
        if action["decision"] == correct["decision"]:
            score += 0.5

        # Score match (tolerance)
        if abs(action["score"] - correct["score"]) < 0.2:
            score += 0.3

        # Reason quality
        if len(action["reason"]) > 10:
            score += 0.2

        done = True

        return Observation(job_description="", resume=""), score, done, {}

    def state(self):
        return self.current