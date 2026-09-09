"""
Recommendation API routes for EduMatch AI / Smart Education.
Exposes endpoints for generating personalized recommendations and querying resources,
with support for study time constraints and download options.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from engine.recommender import recommend_resources, load_resources

router = APIRouter(prefix="/api", tags=["Recommendations & Resources"])


class StudentProfile(BaseModel):
    name: Optional[str] = Field(default="Learner", description="Student's display name")
    subject: str = Field(..., example="Python", description="Subject the student wants to learn")
    level: str = Field(..., example="Beginner", description="Current mastery level: Beginner, Intermediate, or Advanced")
    goal: str = Field(..., example="Exam Preparation", description="Primary goal: Exam Preparation, Concept Understanding, Practice, or Project Building")
    preferred_type: Optional[str] = Field(default=None, example="Video", description="Optional preferred resource format: Video, Notes, PPT, Quiz, Interactive Practice, Course")
    max_duration_minutes: Optional[int] = Field(default=None, example=60, description="Available study time in minutes (e.g. 30, 45, 60, 120)")
    preferred_time: Optional[str] = Field(default=None, example="1 hr", description="Alternative text representation of available time")
    top_n: Optional[int] = Field(default=5, ge=1, le=20, description="Maximum number of recommendations to return")
    min_score: Optional[float] = Field(default=20.0, ge=0.0, le=100.0, description="Minimum match percentage threshold")


@router.post("/recommendations")
def get_recommendations(profile: StudentProfile):
    """
    Generate personalized learning resource recommendations for a student profile.
    Connects to the multi-factor scoring engine and explainable AI generator.
    Enforces time constraints (e.g. videos <= preferred study time) and format preferences.
    """
    try:
        results = recommend_resources(
            student=profile.model_dump(),
            top_n=profile.top_n or 5,
            min_score=profile.min_score or 20.0
        )
        return {
            "success": True,
            "data": results
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Recommendation engine error: {str(exc)}")


@router.get("/resources")
def get_all_resources(
    subject: Optional[str] = Query(default=None, description="Filter by subject"),
    level: Optional[str] = Query(default=None, description="Filter by level"),
    type: Optional[str] = Query(default=None, description="Filter by resource type"),
    max_duration: Optional[int] = Query(default=None, description="Filter resources taking at most N minutes"),
):
    """
    Retrieve all available learning resources with optional filtering.
    """
    resources = load_resources()

    if subject:
        resources = [r for r in resources if r.get("subject", "").lower() == subject.lower()]
    if level:
        resources = [r for r in resources if r.get("level", "").lower() == level.lower()]
    if type:
        resources = [r for r in resources if r.get("type", "").lower() == type.lower()]
    if max_duration:
        resources = [r for r in resources if (r.get("duration_minutes") or 9999) <= max_duration]

    return {
        "success": True,
        "count": len(resources),
        "data": resources
    }


@router.get("/meta")
def get_metadata():
    """
    Returns available subjects, levels, goals, types, and time presets to power frontend form selectors.
    """
    resources = load_resources()

    subjects = sorted(list({r.get("subject") for r in resources if r.get("subject")}))
    levels = ["Beginner", "Intermediate", "Advanced"]
    goals = ["Exam Preparation", "Concept Understanding", "Practice", "Project Building"]
    types = ["Video", "Notes", "PPT", "Interactive Practice", "Quiz", "Course"]
    time_presets = [
        {"label": "Any duration (no limit)", "minutes": None},
        {"label": "25 - 30 Minutes (Quick Sprint)", "minutes": 30},
        {"label": "45 Minutes (Class Period)", "minutes": 45},
        {"label": "1 Hour (Standard Session)", "minutes": 60},
        {"label": "1.5 Hours (Deep Study)", "minutes": 90},
        {"label": "2 Hours (Intensive)", "minutes": 120},
        {"label": "3+ Hours (Masterclass)", "minutes": 180},
    ]

    return {
        "success": True,
        "subjects": subjects,
        "levels": levels,
        "goals": goals,
        "types": types,
        "time_presets": time_presets
    }
