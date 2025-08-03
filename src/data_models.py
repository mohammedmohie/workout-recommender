"""
Data models for the Workout Recommender System
"""

from typing import List, Optional, Dict, Any

from pydantic import BaseModel


class UserProfile(BaseModel):
    user_id: str
    name: str
    age: int
    gender: str
    goal: str
    fitness_level: str
    injuries: List[str]
    preferred_workouts: List[str]
    equipment: List[str]
    past_workouts: Optional[List[Dict[str, Any]]] = None


class Exercise(BaseModel):
    name: str
    exercise_type: str
    muscle_groups: List[str]
    equipment_needed: List[str]
    intensity: str
    difficulty: str
    injury_restrictions: List[str]
    alternatives: List[str]


class WorkoutTemplate(BaseModel):
    goal: str
    structure: Dict[str, int]  # workout_type: count


class WorkoutPlan(BaseModel):
    user_id: str
    week_number: int
    days: Dict[str, Dict[str, Any]]
