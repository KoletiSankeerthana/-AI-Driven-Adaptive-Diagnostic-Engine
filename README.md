
# AI-Driven Adaptive Diagnostic Engine

## 1. Project Overview

The **AI-Driven Adaptive Diagnostic Engine** is a backend system that dynamically evaluates a student's ability level by adapting the difficulty of questions based on their previous responses.

Instead of giving every student the same static test, this system continuously estimates the student's **ability score** and selects the **most appropriate next question**.

After the diagnostic test finishes, the system generates a **personalized AI-powered study plan** using an LLM to help the student improve their weak areas.

This prototype demonstrates the core architecture behind **adaptive learning platforms used by systems like GRE, GMAT, and modern EdTech platforms**.

---

# 2. Key Features

• Adaptive question selection based on user ability
• Dynamic ability score estimation using simplified **Item Response Theory (IRT)**
• MongoDB based question bank and session tracking
• FastAPI backend with modular architecture
• AI-generated personalized study plan
• Clean API design with Swagger documentation
• Scalable backend architecture

---

# 3. System Architecture

The system follows a **modular backend architecture**.

```
Client / Frontend
        ↓
FastAPI API Layer
        ↓
Adaptive Testing Engine
        ↓
MongoDB Database
        ↓
AI Study Plan Generator (OpenAI API)
```

### Components

**FastAPI**

* Handles REST API requests
* Provides interactive Swagger API testing

**MongoDB**

* Stores questions
* Stores user sessions
* Tracks answered questions

**Adaptive Engine**

* Calculates user ability score
* Selects optimal next question
* Implements simplified IRT logic

**AI Service**

* Uses OpenAI API
* Generates personalized learning plan

---

# 4. Project Structure

```
adaptive-diagnostic-engine
│
├── app
│   ├── main.py
│   ├── database
│   │     └── mongodb.py
│   ├── models
│   │     └── schemas.py
│   ├── routes
│   │     ├── session_routes.py
│   │     └── question_routes.py
│   └── services
│         ├── adaptive_engine.py
│         └── ai_service.py
│
├── scripts
│   └── seed_questions.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

# 5. Adaptive Algorithm Logic

The diagnostic engine uses a simplified **1-Dimensional Item Response Theory (IRT) model**.

### Step 1 — Session Initialization

Every user session starts with:

```
ability_score = 0.5
```

This represents a **medium baseline ability**.

---

### Step 2 — Adaptive Question Selection

The system retrieves questions from MongoDB and selects the one whose difficulty is closest to the user's ability.

```
| difficulty − ability | → minimum
```

Example:

| User Ability | Question Difficulty Selected |
| ------------ | ---------------------------- |
| 0.5          | 0.5                          |
| 0.6          | 0.6                          |
| 0.7          | 0.7                          |

Previously answered questions are excluded.

---

### Step 3 — Ability Score Update

When the user answers a question, the ability score is updated using:

```
P(correct) = 1 / (1 + exp(-(ability − difficulty)))
```

Then the ability is updated:

```
ability_new = ability + learning_rate * (actual − P(correct))
```

Where:

```
learning_rate = 0.1
actual = 1 if correct
actual = 0 if incorrect
```

---

### Step 4 — Test Completion

The diagnostic test automatically stops after:

```
10 questions
```

This keeps the test short while still estimating ability.

---

# 6. Tech Stack

| Component       | Technology  |
| --------------- | ----------- |
| Backend         | FastAPI     |
| Database        | MongoDB     |
| Language        | Python 3.10 |
| Data Validation | Pydantic    |
| AI Integration  | OpenAI API  |
| Server          | Uvicorn     |

---

# 7. API Documentation

## 1️⃣ Start Session

Creates a new diagnostic session.

```
POST /session/start-session
```

Response

```
{
 "session_id": "uuid-session-id"
}
```

---

## 2️⃣ Get Next Adaptive Question

Returns the next question based on user ability.

```
GET /question/next/{session_id}
```

Example response

```
{
 "question_id": "64bc01f8e13d9abcde123456",
 "question": "What are the solutions to x^2 - 16 = 0?",
 "options": ["4", "-4", "4 and -4", "16"],
 "difficulty": 0.5
}
```

---

## 3️⃣ Submit Answer

Evaluates answer and updates ability score.

```
POST /question/submit-answer
```

Request

```
{
 "session_id": "session-id",
 "question_id": "question-id",
 "answer": "4 and -4"
}
```

Response

```
{
 "correct": true,
 "updated_ability": 0.55
}
```

---

## 4️⃣ Generate Study Plan

Generates AI-powered learning recommendations.

```
GET /session/study-plan/{session_id}
```

Response

```
{
 "study_plan": [
   "Review Algebra fundamentals",
   "Practice medium difficulty GRE questions",
   "Take timed quizzes to improve speed"
 ]
}
```

---

# 8. Setup Instructions

## Step 1 — Install Dependencies

```
pip install -r requirements.txt
```

---

## Step 2 — Configure Environment Variables

Create `.env` file:

```
MONGO_URI=mongodb://localhost:27017
OPENAI_API_KEY=your_openai_api_key
PORT=8000
ENVIRONMENT=development
```

---

## Step 3 — Seed Question Database

```
python scripts/seed_questions.py
```

This loads GRE-style questions into MongoDB.

---

## Step 4 — Run Server

```
uvicorn app.main:app --reload
```

Server runs at:

```
http://localhost:8000
```

Swagger API docs available at:

```
http://localhost:8000/docs
```

---

# 9. Example Test Flow

1️⃣ Start session

```
POST /session/start-session
```

2️⃣ Get first question

```
GET /question/next/{session_id}
```

3️⃣ Submit answer

```
POST /question/submit-answer
```

4️⃣ System updates ability

5️⃣ Next question selected adaptively

6️⃣ After 10 questions → generate study plan

---

## 10. AI Log

AI tools such as **Cursor AI** and **ChatGPT** were used during development to accelerate the engineering process.

### AI assistance was used for:

- Generating the FastAPI project structure  
- Writing MongoDB database connection utilities  
- Designing Pydantic request/response models  
- Implementing the adaptive algorithm logic  
- Generating the GRE question seeding script  
- Creating OpenAI integration for study plan generation  
- Improving error handling and modular code organization  

### Challenges AI Could Not Fully Solve

Some aspects required manual debugging and reasoning:

- Handling MongoDB session state updates correctly  
- Preventing previously answered questions from repeating  
- Adjusting the IRT ability update logic  
- Managing OpenAI API errors and quota handling  
- Ensuring clean API endpoint separation  

AI accelerated development, but final integration and debugging required manual intervention.
---

# Repository

GitHub Repository

```
https://github.com/KoletiSankeerthana/-AI-Driven-Adaptive-Diagnostic-Engine
```

---
