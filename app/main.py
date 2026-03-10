"""
Main application module.
Initializes the FastAPI application and includes routers.
"""
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from app.database.connection import DatabaseClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Adaptive Diagnostic Engine",
    description="A production-style Python backend for an AI-driven adaptive diagnostic engine.",
    version="0.1.0"
)

@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Simple health check endpoint to verify the API is running.
    """
    return {
        "status": "running"
    }

@app.get("/health/db", tags=["Health"])
async def db_health_check() -> dict:
    """
    Verify the database connection.
    """
    try:
        # The ismaster command is cheap and does not require auth.
        client = DatabaseClient.get_client()
        client.admin.command('ismaster')
        return {"database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

# Include routers
from app.routes.session_routes import router as session_router
from app.routes.question_routes import router as question_router

app.include_router(session_router)
app.include_router(question_router)
