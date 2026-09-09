"""
EduMatch AI Recommendation Engine Package
Contains scoring, recommendation orchestration, and explainable AI modules.
"""

from .scoring import calculate_resource_score
from .explanation import generate_recommendation_explanation
from .recommender import recommend_resources

__all__ = [
    "calculate_resource_score",
    "generate_recommendation_explanation",
    "recommend_resources",
]
