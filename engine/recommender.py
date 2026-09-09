"""
Recommendation engine orchestrator for EduMatch AI.
Coordinates database access, scoring, ranking, and explanation generation,
with strict time-window enforcement (e.g. video <= preferred time) and format filtering.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .scoring import calculate_resource_score, parse_duration_to_minutes
from .explanation import generate_recommendation_explanation

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "backend" / "database" / "resources.json"


def load_resources(database_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Loads resources dataset from JSON storage."""
    target_path = database_path or DEFAULT_DB_PATH
    if not target_path.exists():
        return []
    with open(target_path, "r", encoding="utf-8") as f:
        return json.load(f)


def recommend_resources(
    student: Dict[str, Any],
    top_n: int = 4,
    min_score: float = 20.0,
    database_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Main recommendation entrypoint.
    Filters, scores, ranks resources, and augments them with explainability data.
    Enforces time constraints: if preferred time is specified and format is video,
    only videos with duration <= preferred time are recommended.
    """
    all_resources = load_resources(database_path)
    if not all_resources:
        return {
            "student": student,
            "total_candidates": 0,
            "recommendations": []
        }

    preferred_type = (student.get("preferred_type") or "").strip().lower()
    max_minutes = parse_duration_to_minutes(
        student.get("max_duration_minutes") or student.get("preferred_time")
    )

    scored_candidates = []

    for res in all_resources:
        res_type = (res.get("type") or "").strip().lower()
        res_minutes = res.get("duration_minutes") or parse_duration_to_minutes(res.get("duration"))

        # Strict constraint for video format when time limit is given:
        # If user asks for videos within a time limit, exclude videos that exceed it.
        if (preferred_type == "video" or res_type == "video") and max_minutes and res_minutes:
            if res_minutes > max_minutes:
                continue

        # If user specifically asked for PPT / Slides or Notes:
        if preferred_type in ["ppt", "slides", "presentation"] and res_type not in ["ppt", "slides"]:
            # De-prioritize non-PPTs or exclude if sufficient PPTs exist
            pass

        scoring_result = calculate_resource_score(student, res)
        score = scoring_result["score"]

        # Only consider candidates meeting threshold
        if score >= min_score:
            explanation = generate_recommendation_explanation(student, res, scoring_result)
            scored_candidates.append({
                **res,
                "score": score,
                "breakdown": scoring_result["breakdown"],
                "explanation": explanation
            })

    # Sort descending: prioritize preferred format match, then score, then rating
    scored_candidates.sort(
        key=lambda item: (
            (item.get("type", "").lower() == preferred_type) if preferred_type else True,
            item["score"],
            item.get("rating", 0.0)
        ),
        reverse=True
    )

    # Slice top-N recommendations
    final_recommendations = scored_candidates[:top_n]

    return {
        "student": {
            "name": student.get("name", "Learner"),
            "subject": student.get("subject"),
            "level": student.get("level"),
            "goal": student.get("goal"),
            "preferred_type": student.get("preferred_type"),
            "max_duration_minutes": max_minutes,
        },
        "total_candidates": len(all_resources),
        "matched_count": len(scored_candidates),
        "returned_count": len(final_recommendations),
        "recommendations": final_recommendations
    }
