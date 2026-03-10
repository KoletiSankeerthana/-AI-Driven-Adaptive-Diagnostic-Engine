# AI-Driven Adaptive Diagnostic Engine

## 1. Project Overview
The AI-Driven Adaptive Diagnostic Engine is a backend service designed to provide a personalized, adaptive testing experience. It dynamically assesses a user's ability level by serving questions tailored to their changing proficiency as they progress through the test. Upon completion, the engine generates a highly personalized, AI-powered study plan to help the user improve on identified weak areas.

## 2. System Architecture
The project utilizes a clean, modular architecture:
- **FastAPI**: Serves as the robust, high-performance web framework handling RESTful API requests.
- **MongoDB**: The NoSQL database storing the question bank, user session states, and test responses.
- **Adaptive Engine**: Core business logic (housed in `services/adaptive_engine.py`) responsible for calculating ability scores and selecting optimal questions.
- **AI Service**: Integrates with the OpenAI API to analyze test results and generate customized study plans.

## 3. Adaptive Algorithm Logic
The diagnostic test behaves as a 1-D adaptive prototype using a simplified Item Response Theory (IRT) model:
- **Initialization**: Every user session starts with a baseline `ability_score` of `0.5`.
- **Question Selection**: The engine fetches questions from MongoDB, excluding previously answered ones, and selects the question whose `difficulty` rating (0.1 - 1.0) is mathematically closest to the user's current ability score.
- **Score Updating**: After each submitted answer, the ability score is recalculated using:
  - `P(correct) = 1 / (1 + exp(-(ability - difficulty)))`
  - `ability_new = ability + learning_rate * (actual - P(correct))` where `learning_rate = 0.1`.
- The test is automatically capped at a maximum of 10 questions.

## 4. Tech Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: MongoDB (via `pymongo`)
- **Data Validation**: Pydantic
- **AI Integration**: OpenAI API (`gpt-4o`)

## 5. API Documentation

### `POST /session/start-session`
Creates a new test session and initializes the user's ability score to a baseline of 0.5.

**Example Request:**
```http
POST /session/start-session
Host: localhost:8000
```

**Example Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

### `GET /question/next/{session_id}`
Returns the next adaptive question dynamically selected based on the user's calculated ability score. If the session is finished, it returns a completion message.

**Example Request:**
```http
GET /question/next/123e4567-e89b-12d3-a456-426614174000
Host: localhost:8000
```

**Example Response:**
```json
{
  "question_id": "64bc01f8e13d9abcde123456",
  "question": "What are the solutions to x^2 - 16 = 0?",
  "options": ["4", "-4", "4 and -4", "16"],
  "difficulty": 0.5
}
```

---

### `POST /question/submit-answer`
Submits the user's answer, precisely checks whether the answer is mathematically correct, and then iteratively updates their overall ability score according to the internal IRT logic.

**Example Request:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "question_id": "64bc01f8e13d9abcde123456",
  "answer": "4 and -4"
}
```

**Example Response:**
```json
{
  "correct": true,
  "updated_ability": 0.55
}
```

---

### `GET /session/study-plan/{session_id}`
Generates a personalized, 3-step study plan fueled by OpenAI's API. The plan algorithm analyzes performance, correctness, and difficult ceilings to identify and target weaknesses appropriately.

**Example Request:**
```http
GET /session/study-plan/123e4567-e89b-12d3-a456-426614174000
Host: localhost:8000
```

**Example Response:**
```json
{
  "study_plan": [
    "Step 1: Review Algebra fundamentals, particularly solving quadratic equations and isolating variables.",
    "Step 2: Practice GRE-style Algebra questions targeting medium difficulty (0.5 to 0.7) to build confidence.",
    "Step 3: Take a 15-minute timed quiz exclusively composed of Algebra questions to improve both accuracy and speed."
  ]
}
```

## 6. Setup Instructions

1. **Clone and Install Dependencies**
   It's recommended to create a virtual environment first.
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   Ensure your `.env` file is present in the root directory with the following variables:
   ```env
   MONGO_URI=mongodb://localhost:27017
   OPENAI_API_KEY=your_openai_api_key_here
   PORT=8000
   ENVIRONMENT=development
   ```

3. **Database Seeding (Optional)**
   You can populate the MongoDB `adaptive_test_db` with initial GRE-style questions by running:
   ```bash
   python scripts/seed_questions.py
   ```

4. **Run the Application**
   Start the FastAPI server utilizing uvicorn with live code reloading:
   ```bash
   uvicorn app.main:app --reload
   ```
   Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive Swagger UI.

## 7. AI Log
During development, AI-assisted coding was utilized to:
- Generate the core boilerplate adhering to strict clean architecture principles.
- Formulate the complex Pydantic models with advanced field validators.
- Scaffold the mock GRE question database seeding script.
- Engineer the IRT (Item Response Theory) logic block dynamically adjusting the user's state.
- Write robust error handling to fallback to localized study plans upon OpenAI API failures or quota exhaustion.
