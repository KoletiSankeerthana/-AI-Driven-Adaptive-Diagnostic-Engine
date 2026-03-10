
# 🚀 AI-Driven Adaptive Diagnostic Engine

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

An AI-powered backend system that dynamically evaluates a student's ability level through **adaptive testing** and generates a **personalized study plan**.

Unlike traditional static exams, this system adjusts the difficulty of each question based on the user's previous responses, enabling a more accurate assessment of their proficiency.

The project demonstrates the core architecture used in **adaptive learning platforms like GRE, GMAT, and modern EdTech systems**.


---

# 📌 Project Overview

The **AI-Driven Adaptive Diagnostic Engine** is designed to make assessments smarter by dynamically selecting questions based on a student’s ability level.

The system works by:

1. Starting with a baseline ability score
2. Dynamically selecting questions based on ability
3. Updating the ability score after each answer
4. Generating an **AI-powered personalized study plan** at the end of the test

This enables a **short but highly informative diagnostic test**.

---

# 🛠 Installation & Setup

Follow these steps to run the project locally.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/KoletiSankeerthana/-AI-Driven-Adaptive-Diagnostic-Engine.git
```

Move into the project directory:

```bash
cd -AI-Driven-Adaptive-Diagnostic-Engine
```

---

## 2️⃣ Create Virtual Environment (Recommended)

Create virtual environment:

```bash
python -m venv venv
```

Activate it

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Copy the example environment file.

### Mac / Linux

```bash
cp .env.example .env
```

### Windows

```bash
copy .env.example .env
```

Edit `.env` and add your configuration:

```env
MONGO_URI=mongodb://localhost:27017
OPENAI_API_KEY=your_openai_api_key
PORT=8000
ENVIRONMENT=development
```

---

## 5️⃣ Seed the Question Database

Populate MongoDB with sample GRE-style questions:

```bash
python scripts/seed_questions.py
```

---

## 6️⃣ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

# 🖥 Demo

Once the server is running, open the Swagger interface:

```
http://localhost:8000/docs
```

This interactive interface allows you to test the adaptive engine.

---

## Example Workflow

### 1️⃣ Start a Session

```
POST /session/start-session
```

Response:

```json
{
  "session_id": "uuid-session-id"
}
```

---

### 2️⃣ Fetch Next Adaptive Question

```
GET /question/next/{session_id}
```

The system selects the question whose difficulty is closest to the user's ability.

Example response:

```json
{
  "question_id": "64bc01f8e13d9abcde123456",
  "question": "What are the solutions to x^2 - 16 = 0?",
  "options": ["4","-4","4 and -4","16"],
  "difficulty": 0.5
}
```

---

### 3️⃣ Submit an Answer

```
POST /question/submit-answer
```

Example request:

```json
{
  "session_id": "session-id",
  "question_id": "question-id",
  "answer": "4 and -4"
}
```

Example response:

```json
{
  "correct": true,
  "updated_ability": 0.55
}
```

---

### 4️⃣ Adaptive Difficulty Adjustment

After each answer:

* ability score updates
* next question difficulty adapts

---

### 5️⃣ Generate AI Study Plan

After the test completes:

```
GET /session/study-plan/{session_id}
```

Example response:

```json
{
  "study_plan": [
    "Review Algebra fundamentals",
    "Practice medium difficulty GRE questions",
    "Take timed quizzes to improve speed"
  ]
}
```

---

# 🏗 System Architecture

The project follows a **modular backend architecture**.

```
Client (Swagger UI / API Consumer)
        ↓
FastAPI Application Layer
        ↓
Adaptive Testing Engine
        ↓
MongoDB Database
        ↓
AI Study Plan Generator (OpenAI API)
```

---

## Components

### FastAPI

Handles REST API requests and exposes endpoints.

### MongoDB

Stores questions, user sessions, and answers.

### Adaptive Engine

Core logic for:

* ability score calculation
* question selection
* difficulty adjustment

### AI Service

Uses OpenAI API to generate personalized study plans.

---

# 📁 Project Structure

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
├── .env.example
└── docs/images
```

---

# 🧠 Adaptive Algorithm Logic

The engine implements a simplified **1-Dimensional Item Response Theory (IRT)** model.

---

## Step 1 — Session Initialization

Every session begins with:

```
ability_score = 0.5
```

This represents a **medium difficulty baseline**.

---

## Step 2 — Adaptive Question Selection

The system selects the question whose difficulty is closest to the user’s ability.

```
| difficulty − ability | → minimum
```

Example:

| Ability | Question Difficulty |
| ------- | ------------------- |
| 0.5     | 0.5                 |
| 0.6     | 0.6                 |
| 0.7     | 0.7                 |

---

## Step 3 — Ability Score Update

Probability of correct answer:

```
P(correct) = 1 / (1 + exp(-(ability − difficulty)))
```

Ability update:

```
ability_new = ability + learning_rate * (actual − P(correct))
```

Where

```
learning_rate = 0.1
actual = 1 if correct
actual = 0 if incorrect
```

---

## Step 4 — Test Completion

The test stops automatically after:

```
10 questions
```

---

# 🔌 API Endpoints

| Endpoint                           | Method | Description             |
| ---------------------------------- | ------ | ----------------------- |
| `/session/start-session`           | POST   | Start new session       |
| `/question/next/{session_id}`      | GET    | Fetch adaptive question |
| `/question/submit-answer`          | POST   | Submit answer           |
| `/session/study-plan/{session_id}` | GET    | Generate AI study plan  |

---

# ⚙️ Tech Stack

| Component      | Technology |
| -------------- | ---------- |
| Backend        | FastAPI    |
| Language       | Python     |
| Database       | MongoDB    |
| Validation     | Pydantic   |
| AI Integration | OpenAI API |
| Server         | Uvicorn    |

---

# 🤖 AI Log

AI tools such as **Cursor AI** and **ChatGPT** were used during development to accelerate engineering tasks.

### AI was used for:

* generating FastAPI project structure
* writing MongoDB utilities
* designing Pydantic models
* implementing adaptive algorithm
* generating GRE question dataset
* integrating OpenAI API
* improving error handling

---

### Challenges AI Could Not Fully Solve

Some aspects required manual debugging:

* session state management in MongoDB
* preventing repeated questions
* tuning ability score updates
* handling OpenAI API quota errors
* ensuring clean service architecture

AI accelerated development but final integration required manual reasoning.

---

# 🔗 Repository

```
https://github.com/KoletiSankeerthana/-AI-Driven-Adaptive-Diagnostic-Engine
```
