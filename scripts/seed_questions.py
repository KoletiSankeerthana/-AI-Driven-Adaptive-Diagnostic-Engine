"""
Seed script to insert 20 GRE-style questions into the MongoDB database.
Ensures no duplicates are inserted if they already exist, by checking the 'question' field.
"""
import sys
import os

# Add project root to sys.path to resolve 'app' module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import get_questions_collection

QUESTIONS_DATA = [
    # --- Easy (0.1–0.3): 6 questions ---
    {
        "question": "What is 2x + 4 = 10?",
        "options": ["2", "3", "4", "5"],
        "correct_answer": "3",
        "difficulty": 0.2,
        "topic": "Algebra",
        "tags": ["linear_equations"]
    },
    {
        "question": "What is 15% of 200?",
        "options": ["15", "20", "25", "30"],
        "correct_answer": "30",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["percentages"]
    },
    {
        "question": "What is the area of a square with a side length of 4?",
        "options": ["8", "12", "16", "20"],
        "correct_answer": "16",
        "difficulty": 0.2,
        "topic": "Geometry",
        "tags": ["area", "squares"]
    },
    {
        "question": "Which of the following is a synonym for 'Happy'?",
        "options": ["Sad", "Joyful", "Angry", "Tired"],
        "correct_answer": "Joyful",
        "difficulty": 0.1,
        "topic": "Vocabulary",
        "tags": ["synonyms", "basic_words"]
    },
    {
        "question": "If x - 5 = 15, what is x?",
        "options": ["10", "15", "20", "25"],
        "correct_answer": "20",
        "difficulty": 0.3,
        "topic": "Algebra",
        "tags": ["linear_equations"]
    },
    {
        "question": "Calculate 47 + 25.",
        "options": ["62", "72", "82", "92"],
        "correct_answer": "72",
        "difficulty": 0.1,
        "topic": "Arithmetic",
        "tags": ["addition"]
    },

    # --- Medium (0.4–0.6): 8 questions ---
    {
        "question": "What are the solutions to x^2 - 16 = 0?",
        "options": ["4", "-4", "4 and -4", "16"],
        "correct_answer": "4 and -4",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["quadratics"]
    },
    {
        "question": "What is the greatest common divisor of 24 and 36?",
        "options": ["4", "6", "12", "24"],
        "correct_answer": "12",
        "difficulty": 0.5,
        "topic": "Arithmetic",
        "tags": ["gcd", "number_properties"]
    },
    {
        "question": "What is the circumference of a circle with radius 5?",
        "options": ["5π", "10π", "25π", "20π"],
        "correct_answer": "10π",
        "difficulty": 0.5,
        "topic": "Geometry",
        "tags": ["circles", "circumference"]
    },
    {
        "question": "Which word is a synonym for 'Ephemeral'?",
        "options": ["Permanent", "Fleeting", "Ancient", "Heavy"],
        "correct_answer": "Fleeting",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["synonyms", "advanced_words"]
    },
    {
        "question": "Which word is an antonym for 'Loquacious'?",
        "options": ["Talkative", "Silent", "Taciturn", "Loud"],
        "correct_answer": "Taciturn",
        "difficulty": 0.6,
        "topic": "Vocabulary",
        "tags": ["antonyms", "advanced_words"]
    },
    {
        "question": "If 3(x + 2) = 21, what is x?",
        "options": ["3", "4", "5", "7"],
        "correct_answer": "5",
        "difficulty": 0.4,
        "topic": "Algebra",
        "tags": ["linear_equations"]
    },
    {
        "question": "An item costs $100. It is discounted by 20%, then marked up by 25%. What is the final price?",
        "options": ["100", "95", "105", "120"],
        "correct_answer": "100",
        "difficulty": 0.6,
        "topic": "Arithmetic",
        "tags": ["percentages", "word_problems"]
    },
    {
        "question": "What is the hypotenuse of a right triangle with legs of length 3 and 4?",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "5",
        "difficulty": 0.4,
        "topic": "Geometry",
        "tags": ["right_triangles", "pythagorean_theorem"]
    },

    # --- Hard (0.7–0.9): 6 questions ---
    {
        "question": "If x^2 + y^2 = 25 and xy = 12, what is (x+y)^2?",
        "options": ["37", "49", "61", "144"],
        "correct_answer": "49",
        "difficulty": 0.8,
        "topic": "Algebra",
        "tags": ["polynomials", "identities"]
    },
    {
        "question": "What is the remainder when 3^100 is divided by 5?",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "1",
        "difficulty": 0.9,
        "topic": "Arithmetic",
        "tags": ["remainders", "number_theory"]
    },
    {
        "question": "What is the volume of a right circular cylinder with radius 3 and height 10?",
        "options": ["30π", "60π", "90π", "120π"],
        "correct_answer": "90π",
        "difficulty": 0.7,
        "topic": "Geometry",
        "tags": ["volume", "cylinders"]
    },
    {
        "question": "Which of the following describes a 'Sycophant'?",
        "options": ["A harsh critic", "A loyal friend", "A self-serving flatterer", "A skilled archer"],
        "correct_answer": "A self-serving flatterer",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["definitions", "advanced_words"]
    },
    {
        "question": "Which of the following is a synonym for 'Obfuscate'?",
        "options": ["Clarify", "Confuse", "Enhance", "Destroy"],
        "correct_answer": "Confuse",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["synonyms", "advanced_words"]
    },
    {
        "question": "What are the roots of the quadratic equation x^2 - 5x + 6 = 0?",
        "options": ["1 and 6", "-2 and -3", "2 and 3", "0 and 5"],
        "correct_answer": "2 and 3",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["quadratics", "factoring"]
    }
]

def seed_database() -> None:
    """
    Connects to the database and seeds the question collection.
    Avids duplicates by checking if the question text already exists.
    """
    try:
        collection = get_questions_collection()
        inserted_count = 0

        for question_data in QUESTIONS_DATA:
            # Check if question already exists
            existing_q = collection.find_one({"question": question_data["question"]})
            if not existing_q:
                collection.insert_one(question_data)
                inserted_count += 1
        
        print(f"Successfully inserted {inserted_count} new questions.")
        print(f"Skipped {len(QUESTIONS_DATA) - inserted_count} duplicate questions.")
    
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    seed_database()
