import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Educational Content Generator",
    description="API for generating educational content using Llama Stack",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.lesson_plans import router as lesson_plans_router
from app.api.quizzes import router as quizzes_router
from app.api.content_adaptation import router as content_adaptation_router
from app.api.interactive_scenarios import router as interactive_scenarios_router
from app.api.feedback import router as feedback_router
from app.api.subjects import router as subjects_router

app.include_router(lesson_plans_router, prefix="/api/lesson-plans", tags=["Lesson Plans"])
app.include_router(quizzes_router, prefix="/api/quizzes", tags=["Quizzes"])
app.include_router(content_adaptation_router, prefix="/api/content-adaptation", tags=["Content Adaptation"])
app.include_router(interactive_scenarios_router, prefix="/api/interactive-scenarios", tags=["Interactive Scenarios"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(subjects_router, prefix="/api/subjects", tags=["Subject-Specific Tools"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Educational Content Generator API",
        "endpoints": {
            "Lesson Plans": "/api/lesson-plans",
            "Quizzes": "/api/quizzes",
            "Content Adaptation": "/api/content-adaptation",
            "Interactive Scenarios": "/api/interactive-scenarios",
            "Feedback": "/api/feedback",
            "Subject-Specific Tools": "/api/subjects"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
