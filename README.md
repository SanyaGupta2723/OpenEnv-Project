# 🚀 AI Resume Screening Environment (OpenEnv Project)

## 🧠 Overview

This project simulates a **real-world resume screening system** used by HR teams to evaluate candidates based on job requirements.

An AI agent interacts with this environment using the **OpenEnv standard API (`reset()`, `step()`, `state()`)** and is evaluated based on decision-making quality.

---

## 🎯 Key Features

✨ Real-world task simulation (HR resume screening)
✨ Fully OpenEnv compliant environment
✨ 3 difficulty levels (Easy → Medium → Hard)
✨ Reward-based evaluation (0.0 – 1.0)
✨ Dockerized deployment
✨ Hugging Face Space ready 🚀

---

## 🧩 Tasks Breakdown

### 🟢 Easy Task

* Decide: **Shortlist or Reject**
* Based on resume-job match

---

### 🟡 Medium Task

* Decision + **Score (0–1)**
* Evaluate candidate strength

---

### 🔴 Hard Task

* Decision + Score + **Reasoning**
* Explain why candidate is selected/rejected

---

## ⚙️ Environment Design

### 📥 Observation Space

```json
{
  "job_description": "string",
  "resume": "string"
}
```

### 📤 Action Space

```json
{
  "decision": "shortlist/reject",
  "score": 0-1,
  "reason": "text"
}
```

---

## 🎯 Reward Function

| Criteria          | Score |
| ----------------- | ----- |
| Correct Decision  | +0.5  |
| Accurate Score    | +0.3  |
| Meaningful Reason | +0.2  |

✔ Total Reward: **0.0 – 1.0**

---

## 🔄 OpenEnv API

### 🔹 reset()

Initializes a new resume evaluation task

### 🔹 step(action)

Evaluates agent action and returns:

* observation
* reward
* done
* info

### 🔹 state()

Returns current environment state

---

## 🤖 Baseline Agent

Uses OpenAI API to:

* Analyze resume
* Generate decision
* Compute reward

---

## 🛠️ Tech Stack

* 🐍 Python
* 🤖 OpenAI API
* 📦 Pydantic
* 🐳 Docker
* 🤗 Hugging Face Spaces

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repo

```bash
git clone <your-repo-link>
cd resume-env
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create `.env` File

```env
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4.1-mini
API_BASE_URL=https://api.openai.com/v1
```

⚠️ Never upload `.env` to GitHub

---

### 4️⃣ Run Project

```bash
python inference.py
```

---

## 📊 Sample Output

```
[START]
[STEP]
Job: Frontend Developer
Resume: HTML CSS JS
[END]
Final Score: 0.3
```

---

## 🚀 Deployment

This project is deployed using **Hugging Face Spaces (Docker)**

✔ Fully containerized
✔ Auto-build enabled
✔ Production-ready

---

## 🏆 Evaluation Criteria

* Real-world utility ✅
* Task complexity ✅
* Reward design ✅
* OpenEnv compliance ✅
* Code quality ✅

---

## 🔐 Security Note

❌ API keys are NOT stored in the repository
✔ Use `.env` file for secrets

---

## 💡 Future Improvements

* Better dataset (20+ resumes)
* Advanced scoring logic
* JSON parsing improvements
* UI dashboard

---

## 👩‍💻 Author

**Sanya Gupta** 🚀
AI & ML Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

---
