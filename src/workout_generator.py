"""
Workout Plan Formatting and Generation Utilities
"""

from typing import Dict, Any

from .data_models import UserProfile, WorkoutPlan


def format_workout_plan(workout_plan: WorkoutPlan, user: UserProfile) -> str:
    """Format workout plan for display"""
    output = ["=" * 70, f"PERSONALIZED WORKOUT PLAN FOR {user.name.upper()}", "=" * 70,
              f"Goal: {user.goal} | Fitness Level: {user.fitness_level}",
              f"Injuries: {', '.join(user.injuries) if user.injuries else 'None'}",
              f"Equipment: {', '.join(user.equipment)}", "=" * 70]

    # Header

    # Weekly plan
    for day, workout in workout_plan.days.items():
        output.append(f"\n{day.upper()}")
        output.append("-" * 40)
        output.append(f"Type: {workout['type']}")

        if workout['exercises']:
            output.append("")
            for i, exercise in enumerate(workout['exercises'], 1):
                output.append(f"{i}. {exercise['name']}")
                if 'sets' in exercise:
                    output.append(
                        f"   Sets: {exercise['sets']} | Reps: {exercise['reps']} | Rest: {exercise['rest_period']}")
                if exercise.get('notes'):
                    output.append(f"   Note: {exercise['notes']}")
        else:
            if workout['type'] == "Rest":
                output.append("   Complete rest day - focus on recovery")
            elif workout['type'] == "Active Recovery":
                output.append("   Light stretching or yoga")
            else:
                output.append("   No suitable exercises available")

    return "\n".join(output)


def generate_detailed_plan(workout_plan: WorkoutPlan, user: UserProfile) -> Dict[str, Any]:
    """Generate a detailed workout plan with additional metadata"""
    detailed_plan = {
        "user_info": {
            "user_id": user.user_id,
            "name": user.name,
            "goal": user.goal,
            "fitness_level": user.fitness_level
        },
        "weekly_plan": workout_plan.days,
        "metadata": {
            "generated_at": "2024-01-01",  # In real implementation, use datetime
            "version": "1.0"
        }
    }
    return detailed_plan
