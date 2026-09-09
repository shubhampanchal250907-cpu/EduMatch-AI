"""
Scoring module for EduMatch AI Recommendation Engine.
Calculates multi-dimensional compatibility scores between student profiles and learning resources,
including time-window constraints (e.g. <= 1 hr video recommendation) and format synergy.
"""

import re
from typing import Dict, Any, Optional

LEVEL_ORDER = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
}

GOAL_TYPE_SYNERGY = {
    "practice": ["interactive practice", "quiz", "problem-solving"],
    "concept understanding": ["notes", "video", "course", "documentation", "ppt"],
    "exam preparation": ["notes", "quiz", "interactive practice", "ppt"],
    "project building": ["course", "interactive practice", "tutorial", "ppt"],
}


def parse_duration_to_minutes(duration_val: Any) -> Optional[int]:
    """
    Parses duration representations into integer minutes.
    Examples: 60 -> 60, "1 hr" -> 60, "1.5 hours" -> 90, "45 mins" -> 45.
    """
    if duration_val is None or duration_val == "":
        return None
    if isinstance(duration_val, (int, float)):
        return int(duration_val) if duration_val > 0 else None

    text = str(duration_val).strip().lower()
    if not text:
        return None

    # Try matching hours (e.g. "1.5 hours", "1 hr", "2 hrs")
    hr_match = re.search(r"([\d.]+)\s*(?:hour|hr|h)", text)
    if hr_match:
        try:
            return int(float(hr_match.group(1)) * 60)
        except ValueError:
            pass

    # Try matching minutes (e.g. "45 mins", "30 min", "25m")
    min_match = re.search(r"(\d+)\s*(?:min|m)", text)
    if min_match:
        try:
            return int(min_match.group(1))
        except ValueError:
            pass

    # Plain digits
    try:
        val = int(text)
        return val if val > 0 else None
    except ValueError:
        return None


def calculate_resource_score(student: Dict[str, Any], resource: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes a weighted match score (0-100) between a student and a resource.
    Incorporates:
      - Subject Match: 40%
      - Level Match:   25%
      - Goal Match:    20%
      - Quality/Rating: 15%
      - Time window constraint: enforces resources (especially videos) <= user's preferred time.
      - Format preferences (video, notes, ppt, etc.)
    """
    student_subject = (student.get("subject") or "").strip().lower()
    student_level = (student.get("level") or "").strip().lower()
    student_goal = (student.get("goal") or "").strip().lower()
    preferred_type = (student.get("preferred_type") or "").strip().lower()

    # Parse preferred time limit from student
    max_minutes = parse_duration_to_minutes(
        student.get("max_duration_minutes") or student.get("preferred_time")
    )

    res_subject = (resource.get("subject") or "").strip().lower()
    res_level = (resource.get("level") or "").strip().lower()
    res_type = (resource.get("type") or "").strip().lower()
    res_goals = [g.strip().lower() for g in resource.get("goals", [])]
    res_rating = float(resource.get("rating", 4.0))
    res_tags = [t.strip().lower() for t in resource.get("tags", [])]

    # Resolve resource duration in minutes
    res_minutes = resource.get("duration_minutes") or parse_duration_to_minutes(resource.get("duration"))

    # 1. Subject Score (0.0 to 1.0, 40 points max)
    if student_subject and student_subject == res_subject:
        subject_coeff = 1.0
    elif student_subject and (student_subject in res_subject or any(student_subject in t for t in res_tags)):
        subject_coeff = 0.7
    elif not student_subject:
        subject_coeff = 0.5
    else:
        subject_coeff = 0.0
    subject_score = subject_coeff * 40.0

    # 2. Level Score (0.0 to 1.0, 25 points max)
    s_lvl_idx = LEVEL_ORDER.get(student_level, 2)
    r_lvl_idx = LEVEL_ORDER.get(res_level, 2)
    distance = abs(s_lvl_idx - r_lvl_idx)

    if distance == 0:
        level_coeff = 1.0
    elif distance == 1:
        level_coeff = 0.55
    else:
        level_coeff = 0.15
    level_score = level_coeff * 25.0

    # 3. Goal & Learning Mode Alignment (0.0 to 1.0, 20 points max)
    if student_goal and student_goal in res_goals:
        goal_coeff = 1.0
    elif student_goal and any(res_type in syn for syn in GOAL_TYPE_SYNERGY.get(student_goal, [])):
        goal_coeff = 0.85
    elif not student_goal:
        goal_coeff = 0.6
    else:
        goal_coeff = 0.3
    goal_score = goal_coeff * 20.0

    # 4. Rating & Quality Score (15 points max)
    rating_coeff = min(max(res_rating / 5.0, 0.0), 1.0)
    rating_score = rating_coeff * 15.0

    # 5. Format Preference Boost
    format_bonus = 0.0
    if preferred_type:
        # Match 'ppt' or 'slides'
        if preferred_type in ["ppt", "slides", "presentation"] and res_type in ["ppt", "slides"]:
            format_bonus += 8.0
        elif preferred_type in ["notes", "pdf"] and res_type in ["notes", "pdf"]:
            format_bonus += 8.0
        elif preferred_type == res_type:
            format_bonus += 8.0

    # 6. Time Window Constraint Logic
    time_bonus = 0.0
    time_penalty = 0.0
    time_fits = True
    time_exceeded = False

    if max_minutes and res_minutes:
        if res_minutes <= max_minutes:
            # Fits nicely inside available study window
            time_fits = True
            time_bonus = 6.0
        else:
            time_fits = False
            time_exceeded = True
            # If user explicitly requested video or resource is a video, penalize strongly
            # so videos <= user's time are prioritized or selected as requested.
            if res_type == "video" or preferred_type == "video":
                time_penalty = 50.0  # Major penalty to disqualify over-length videos
            else:
                time_penalty = 20.0

    raw_score = subject_score + level_score + goal_score + rating_score + format_bonus + time_bonus - time_penalty
    total_score = max(0.0, min(round(raw_score, 1), 100.0))

    return {
        "score": total_score,
        "breakdown": {
            "subject_score": round(subject_score, 1),
            "level_score": round(level_score, 1),
            "goal_score": round(goal_score, 1),
            "rating_score": round(rating_score, 1),
            "format_bonus": round(format_bonus, 1),
            "time_bonus": round(time_bonus, 1),
            "time_penalty": round(time_penalty, 1),
            "level_distance": distance,
            "exact_subject": subject_coeff == 1.0,
            "exact_goal": student_goal in res_goals if student_goal else False,
            "time_fits": time_fits,
            "time_exceeded": time_exceeded,
            "res_minutes": res_minutes,
            "max_minutes": max_minutes
        }
    }
