"""
Explanation module for EduMatch AI Recommendation Engine.
Produces clear, personalized rationale and badges explaining why each resource was recommended,
including time-window suitability and download availability for PPTs/Notes.
"""

from typing import Dict, Any, List


def generate_recommendation_explanation(
    student: Dict[str, Any],
    resource: Dict[str, Any],
    scoring_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Constructs a human-readable explanation and key feature badges for a recommendation.
    """
    student_name = student.get("name") or "Learner"
    student_subject = student.get("subject", "")
    student_level = student.get("level", "")
    student_goal = student.get("goal", "")

    res_type = resource.get("type", "Material")
    res_level = resource.get("level", "")
    res_rating = resource.get("rating", 4.5)
    is_downloadable = resource.get("downloadable", False) or res_type in ["Notes", "PPT"]

    breakdown = scoring_result.get("breakdown", {})
    score = scoring_result.get("score", 0.0)
    res_mins = breakdown.get("res_minutes")
    max_mins = breakdown.get("max_minutes")
    time_fits = breakdown.get("time_fits", True)

    reasons: List[str] = []
    badges: List[str] = []

    # Subject alignment
    if breakdown.get("exact_subject"):
        reasons.append(f"Directly covers your target subject '{student_subject}'.")
        badges.append(f"Subject Match: {student_subject}")
    elif student_subject:
        reasons.append(f"Highly relevant companion topic for '{student_subject}'.")
        badges.append("Related Topic")

    # Level alignment
    level_dist = breakdown.get("level_distance", 0)
    if level_dist == 0:
        reasons.append(f"Calibrated specifically for {student_level} proficiency.")
        badges.append(f"Level: {student_level}")
    elif level_dist == 1:
        reasons.append(f"Offers progressive material to help you transition from {student_level} to {res_level}.")
        badges.append(f"Bridge to {res_level}")
    else:
        reasons.append(f"Presents advanced stretch concepts beyond {student_level}.")
        badges.append("Stretch Challenge")

    # Goal alignment
    if breakdown.get("exact_goal"):
        reasons.append(f"Optimized for your objective: '{student_goal}'.")
        badges.append(f"Goal: {student_goal}")
    elif student_goal:
        reasons.append(f"Its {res_type.lower()} format reinforces your '{student_goal}' workflow.")
        badges.append(f"{res_type} Format")

    # Time Window alignment
    if max_mins:
        if time_fits and res_mins:
            reasons.append(f"Fits within your {max_mins}-minute study time limit (Takes ~{res_mins} mins).")
            badges.append(f"Fits Time: {res_mins}m")
        elif not time_fits and res_mins:
            reasons.append(f"Estimated duration (~{res_mins} mins) exceeds your {max_mins}-minute session.")

    # Downloadable badge
    if is_downloadable:
        badges.append(f"Downloadable {res_type}")
        reasons.append(f"Includes direct downloadable {res_type} file for offline study.")

    # Rating badge
    if res_rating >= 4.8:
        badges.append(f"Top Rated: {res_rating}/5.0")

    # Main synthesis summary sentence
    time_phrase = f" and fits inside your {max_mins}m window" if (max_mins and time_fits) else ""
    summary_sentence = (
        f"Hi {student_name}, this {res_type.lower()} is a {score}% match because it directly "
        f"aligns with your {student_level.lower()} study of {student_subject} for {student_goal.lower()}{time_phrase}."
        if (student_subject and student_level and student_goal)
        else f"Curated {res_type.lower()} ({score}% match) tailored for your study schedule."
    )

    return {
        "summary": summary_sentence,
        "reasons": reasons,
        "badges": badges,
        "match_percentage": f"{int(score)}%",
    }
