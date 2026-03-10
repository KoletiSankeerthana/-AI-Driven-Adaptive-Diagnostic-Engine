"""
Database connection module.
Handles connection to MongoDB using pymongo.
"""
import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is missing")

DATABASE_NAME = "adaptive_test_db"

class DatabaseClient:
    """
    Singleton wrapper for MongoDB client to avoid duplicate connections.
    """
    _client: MongoClient | None = None

    @classmethod
    def get_client(cls) -> MongoClient:
        """Initialize or return the existing MongoClient."""
        if cls._client is None:
            cls._client = MongoClient(MONGO_URI)
        return cls._client

    @classmethod
    def get_db(cls) -> Database:
        """Returns the specific database instance."""
        client = cls.get_client()
        return client[DATABASE_NAME]

def get_questions_collection() -> Collection:
    """Helper to access the questions collection."""
    db = DatabaseClient.get_db()
    return db["questions"]

def get_sessions_collection() -> Collection:
    """Helper to access the sessions collection."""
    db = DatabaseClient.get_db()
    return db["user_sessions"]

