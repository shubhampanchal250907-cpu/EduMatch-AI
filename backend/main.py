"""
Main FastAPI server for EduMatch AI / Smart Education recommendation backend.
Handles CORS, routes registration, and application lifecycle.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.routes.recommendation import router as recommendation_router

app = FastAPI(
    title="EduMatch AI - Recommendation Backend",
    description="Intelligent personalized learning resource recommendation API powered by multi-factor scoring & explainable AI.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend applications (React, Vite, Next.js, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(recommendation_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "EduMatch AI Recommendation API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "flow": "Frontend (React) -> Backend (FastAPI) -> Recommendation Engine (Scoring + XAI)"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
