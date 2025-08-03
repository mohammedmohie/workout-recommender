"""
Main Recommender Engine for Workout Plans
"""

import os
from collections import defaultdict
from typing import Dict, List, Any

from .data_models import UserProfile, WorkoutPlan
from .utils import load_json_data


class WorkoutRecommender:
    """Workout plan recommendation engine that generates personalized exercise routines.

    This class handles loading and management of exercise data, workout templates, and
    generates personalized workout plans based on user profiles. It takes into account:
    - User fitness goals
    - Available equipment
    - Injury restrictions
    - Fitness level
    - Exercise intensity and difficulty

    The recommender ensures safe and appropriate exercise selection by filtering exercises
    based on user injuries and available equipment, while following proper workout
    structuring principles like rest periods and exercise variety.

    Attributes:
        data_path (str): Directory path containing exercise and template JSON data files
        exercises (List[Dict]): Database of available exercises and their attributes
        templates (List[Dict]): List of workout templates for different goals
        default_template (Dict): Default template structure for general fitness
        templates (Dict): Collection of workout templates for different fitness goals

    Example:
        recommender = WorkoutRecommender()
        workout_plan = recommender.generate_workout_plan(user_profile)
    """

    def __init__(self, data_path: str = None):
        """Initialize the recommender with exercise and template data.
        
        Args:
            data_path: Directory containing JSON data files. If None, uses default path.
        """
        if data_path is None:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the project root
            project_root = os.path.dirname(current_dir)
            self.data_path = os.path.join(project_root, "data")
        else:
            self.data_path = data_path

        self.exercises = self._load_exercises()
        self.templates = self._load_templates()

    def _load_exercises(self) -> List[Dict[str, Any]]:
        """Load exercise database from JSON file"""
        exercises_path = os.path.join(self.data_path, "exercises.json")
        try:
            data = load_json_data(exercises_path)
            if not data:  # If empty list/dict returned
                return self._get_default_exercises()
            # Extract workouts from the nested structure
            if isinstance(data, dict) and "workouts" in data:
                exercises = data["workouts"]
            else:
                exercises = data
            return exercises if isinstance(exercises, list) else [exercises]
        except Exception as e:
            print(f"Error loading exercises: {str(e)}")
            return self._get_default_exercises()

    def _load_templates(self) -> List[Dict[str, Any]]:
        """Load workout templates from JSON file"""
        default_templates = [{
            "goal": "General Fitness",
            "structure": {
                "Monday": "Strength",
                "Tuesday": "Cardio",
                "Wednesday": "Core",
                "Thursday": "Strength",
                "Friday": "Cardio",
                "Saturday": "Flexibility",
                "Sunday": "Rest"
            }
        }]

        templates_path = os.path.join(self.data_path, "workout_templates.json")
        try:
            data = load_json_data(templates_path)
            if not data:  # If empty list/dict returned
                print("No templates found, using default templates")
                return default_templates
            
            if isinstance(data, dict):
                if "goal" in data:  # Single template
                    return [data]
                else:  # Dictionary of templates
                    return [{"goal": key, **value} for key, value in data.items()]
            elif isinstance(data, list):
                # Validate each template
                valid_templates = []
                for template in data:
                    if isinstance(template, dict) and "goal" in template:
                        valid_templates.append(template)
                
                if valid_templates:
                    return valid_templates
                print("No valid templates found in list, using default templates")
                return default_templates
            else:
                print(f"Unexpected templates format: {type(data)}")
                return default_templates
        except Exception as e:
            print(f"Error loading templates: {str(e)}")
            return default_templates

    def _get_default_exercises(self) -> List[Dict[str, Any]]:
        """Default exercise database"""
        return [
            {
                "name": "Dumbbell Thrusters",
                "exercise_type": "Strength",
                "muscle_groups": ["Legs", "Shoulders"],
                "equipment_needed": ["Dumbbells"],
                "intensity": "High",
                "difficulty": "Intermediate",
                "injury_restrictions": ["Shoulder Issue"],
                "alternatives": ["Bodyweight Squats"]
            },
            {
                "name": "Step-Ups",
                "exercise_type": "Strength",
                "muscle_groups": ["Legs"],
                "equipment_needed": ["Step"],
                "intensity": "Moderate",
                "difficulty": "Beginner",
                "injury_restrictions": ["Knee Injury"],
                "alternatives": ["Bodyweight Squats"]
            },
            {
                "name": "Resistance Band Rows",
                "exercise_type": "Strength",
                "muscle_groups": ["Back"],
                "equipment_needed": ["Resistance Bands"],
                "intensity": "Moderate",
                "difficulty": "Beginner",
                "injury_restrictions": ["Shoulder Issue"],
                "alternatives": ["Seated Rows"]
            },
            {
                "name": "Stationary Bike",
                "exercise_type": "Cardio",
                "muscle_groups": ["Legs"],
                "equipment_needed": ["Stationary Bike"],
                "intensity": "Moderate",
                "difficulty": "Beginner",
                "injury_restrictions": ["Knee Injury"],
                "alternatives": ["Swimming"]
            },
            {
                "name": "Swimming",
                "exercise_type": "Cardio",
                "muscle_groups": ["Full Body"],
                "equipment_needed": ["Pool"],
                "intensity": "Moderate",
                "difficulty": "Beginner",
                "injury_restrictions": [],
                "alternatives": ["Water Aerobics"]
            },
            {
                "name": "Bodyweight Squats",
                "exercise_type": "Strength",
                "muscle_groups": ["Legs"],
                "equipment_needed": [],
                "intensity": "Low",
                "difficulty": "Beginner",
                "injury_restrictions": [],
                "alternatives": ["Wall Sit"]
            },
            {
                "name": "Plank",
                "exercise_type": "Core",
                "muscle_groups": ["Core"],
                "equipment_needed": [],
                "intensity": "Low",
                "difficulty": "Beginner",
                "injury_restrictions": [],
                "alternatives": ["Side Plank"]
            },
            {
                "name": "Elliptical",
                "exercise_type": "Cardio",
                "muscle_groups": ["Full Body"],
                "equipment_needed": ["Elliptical"],
                "intensity": "Moderate",
                "difficulty": "Beginner",
                "injury_restrictions": ["Knee Injury"],
                "alternatives": ["Rowing Machine"]
            }
        ]

    def _get_default_templates(self) -> Dict[str, Any]:
        """Default workout templates"""
        return {
            "Weight Loss": {
                "goal": "Weight Loss",
                "structure": {
                    "HIIT": 3,
                    "Cardio": 2,
                    "Strength": 1,
                    "Flexibility": 1
                }
            },
            "Muscle Gain": {
                "goal": "Muscle Gain",
                "structure": {
                    "Strength": 4,
                    "Core": 1,
                    "Cardio": 1
                }
            },
            "Endurance": {
                "goal": "Endurance",
                "structure": {
                    "Cardio": 3,
                    "Circuit": 2
                }
            },
            "General Fitness": {
                "goal": "General Fitness",
                "structure": {
                    "Strength": 2,
                    "Cardio": 2,
                    "Flexibility": 1,
                    "Core": 1
                }
            },
            "Rehabilitation": {
                "goal": "Rehabilitation",
                "structure": {
                    "Mobility": 3,
                    "Flexibility": 2,
                    "Low-Impact": 2
                }
            }
        }

    def _filter_exercises_by_injury(self, exercises: List[Dict], injuries: List[str]) -> List[Dict]:
        """Filter exercises based on user injuries"""
        safe_exercises = []
        for exercise in exercises:
            # Check if any restriction conflicts with user injuries
            conflict = False
            for restriction in exercise.get("injury_restrictions", []):
                if restriction in injuries:
                    conflict = True
                    break
            if not conflict:
                safe_exercises.append(exercise)
        return safe_exercises

    def _filter_exercises_by_equipment(self, exercises: List[Dict], equipment: List[str]) -> List[Dict]:
        """Filter exercises based on available equipment"""
        available_exercises = []
        for exercise in exercises:
            required_equipment = exercise.get("equipment_needed", [])
            # If no equipment needed, it's available
            if not required_equipment:
                available_exercises.append(exercise)
            # If equipment needed, check if user has it
            else:
                has_equipment = any(eq in equipment for eq in required_equipment)
                if has_equipment:
                    available_exercises.append(exercise)
        return available_exercises

    def _categorize_exercises(self, exercises: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize exercises by type"""
        categorized = defaultdict(list)
        for exercise in exercises:
            exercise_type = exercise.get("exercise_type", "Other")
            categorized[exercise_type].append(exercise)
        return dict(categorized)

    def _get_workout_template(self, goal: str) -> Dict[str, Any]:
        """Get workout template for user goal"""
        # Default template structure
        default_template = {
            "goal": "General Fitness",
            "structure": {
                "Monday": "Strength",
                "Tuesday": "Cardio",
                "Wednesday": "Core",
                "Thursday": "Strength",
                "Friday": "Cardio",
                "Saturday": "Flexibility",
                "Sunday": "Rest"
            }
        }
        
        # Find the latest template for the goal
        template = None
        if isinstance(self.templates, list):
            # Search for exact match
            for t in reversed(self.templates):  # Reverse to get latest first
                if isinstance(t, dict) and t.get("goal") == goal:
                    template = t.copy()  # Make a copy to avoid modifying original
                    break
            
            # If no match found, try General Fitness
            if not template:
                for t in reversed(self.templates):
                    if isinstance(t, dict) and t.get("goal") == "General Fitness":
                        template = t.copy()
                        break
        
        # If still no template, use default
        if not template:
            template = default_template
        
        # Ensure template has proper structure
        if not isinstance(template.get("structure"), dict):
            template["structure"] = default_template["structure"]
        else:
            # Convert frequency-based to day-based if needed
            structure = template["structure"]
            if not any(day in structure for day in ["Monday", "Tuesday", "Wednesday"]):
                template["structure"] = default_template["structure"]
        
        return template

    def _apply_user_preferences(self, exercises: List[Dict], 
                                preferred_types: List[str] = None,
                                fitness_level: str = "Beginner",
                                past_workouts: List[Dict] = None) -> List[Dict]:
        """Apply user preferences to exercise selection based on past workout history"""
        if not exercises:
            return []
            
        if preferred_types is None:
            preferred_types = []
            
        if past_workouts is None:
            past_workouts = []
            
        # Analyze past workout preferences
        type_satisfaction = {}
        intensity_satisfaction = {}
        for workout in past_workouts:
            if workout.get('completed'):
                w_type = workout.get('workout_type')
                satisfaction = workout.get('satisfaction', 3)
                intensity = workout.get('intensity')
                
                if w_type:
                    if w_type not in type_satisfaction:
                        type_satisfaction[w_type] = []
                    type_satisfaction[w_type].append(satisfaction)
                    
                if intensity:
                    if intensity not in intensity_satisfaction:
                        intensity_satisfaction[intensity] = []
                    intensity_satisfaction[intensity].append(satisfaction)
        
        # Calculate average satisfaction for each type and intensity
        avg_type_satisfaction = {
            t: sum(scores)/len(scores) 
            for t, scores in type_satisfaction.items()
        }
        avg_intensity_satisfaction = {
            i: sum(scores)/len(scores) 
            for i, scores in intensity_satisfaction.items()
        }
            
        # Score exercises
        scored_exercises = []
        for exercise in exercises:
            score = 0
            
            # Match exercise type with preferences
            exercise_type = exercise.get('exercise_type', '')
            if exercise_type and exercise_type in preferred_types:
                score += 2
                
            # Match difficulty with fitness level
            if exercise.get('difficulty') == fitness_level:
                score += 1
            
            # Consider exercise attributes
            if exercise.get('sets') and exercise.get('reps'):
                score += 0.5  # Prefer exercises with detailed parameters
                
            # Consider intensity appropriateness and past satisfaction
            intensity = exercise.get('intensity', 'Moderate')
            if intensity in avg_intensity_satisfaction:
                satisfaction_score = avg_intensity_satisfaction[intensity]
                if satisfaction_score >= 4:  # User really liked this intensity
                    score += 2
                elif satisfaction_score >= 3:  # User was okay with this intensity
                    score += 1
                    
            # Consider past workout type satisfaction
            ex_type = exercise.get('exercise_type')
            if ex_type in avg_type_satisfaction:
                type_satisfaction_score = avg_type_satisfaction[ex_type]
                if type_satisfaction_score >= 4:  # User really liked this type
                    score += 2
                elif type_satisfaction_score >= 3:  # User was okay with this type
                    score += 1
                    
            # Adjust based on fitness level and intensity match
            if fitness_level == "Beginner" and intensity == "Low":
                score += 1
            elif fitness_level == "Intermediate" and intensity == "Moderate":
                score += 1
            elif fitness_level == "Advanced" and intensity == "High":
                score += 1
                
            scored_exercises.append((score, exercise))
        
        # Sort by score and use exercise name as secondary key for stable sorting
        sorted_exercises = [ex for _, ex in sorted(
            scored_exercises,
            key=lambda x: (x[0], x[1].get('name', '')),
            reverse=True
        )]
        return sorted_exercises

    def _balance_muscle_groups(self, categorized_exercises: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """Ensure balanced distribution of muscle groups"""
        balanced = {}
        
        for workout_type, exercises in categorized_exercises.items():
            muscle_group_count = defaultdict(int)
            balanced_exercises = []
            
            # Count exercises per muscle group, skip if missing
            for exercise in exercises:
                for muscle in exercise.get('muscle_groups', []):
                    muscle_group_count[muscle] += 1
            
            # Balance selection
            selected_muscles = set()
            for exercise in exercises:
                # Prioritize underrepresented muscle groups, skip if missing
                muscle_groups = exercise.get('muscle_groups', [])
                if not any(muscle in selected_muscles for muscle in muscle_groups):
                    balanced_exercises.append(exercise)
                    selected_muscles.update(muscle_groups)
            
            # Add remaining exercises
            remaining = [ex for ex in exercises if ex not in balanced_exercises]
            balanced_exercises.extend(remaining)
            
            balanced[workout_type] = balanced_exercises
        return balanced

    def _generate_progressive_parameters(self, fitness_level: str, goal: str) -> Dict[str, Any]:
        """Generate progressive workout parameters based on user level and goal"""
        base_params = {
            "Beginner": {
                "sets": {"min": 2, "max": 3},
                "reps": {"min": 8, "max": 12},
                "rest": {"min": 60, "max": 90}
            },
            "Intermediate": {
                "sets": {"min": 3, "max": 4},
                "reps": {"min": 10, "max": 15},
                "rest": {"min": 45, "max": 75}
            },
            "Advanced": {
                "sets": {"min": 3, "max": 5},
                "reps": {"min": 12, "max": 20},
                "rest": {"min": 30, "max": 60}
            }
        }
        
        # Adjust based on goal
        params = base_params.get(fitness_level, base_params["Beginner"]).copy()
        if goal == "Muscle Gain":
            params["sets"]["min"] += 1
            params["rest"]["max"] += 15
        elif goal == "Endurance":
            params["reps"]["min"] += 4
            params["reps"]["max"] += 4
            params["rest"]["max"] -= 15
        
        return params

    def _adapt_template_to_preferences(self, template: Dict[str, Any],
                                    preferred_types: List[str] = None,
                                    fitness_level: str = "Beginner") -> Dict[str, Any]:
        """Adapt workout template based on user preferences"""
        if template is None:
            # Create a default template if none provided
            template = {
                "structure": {
                    "Monday": "Strength",
                    "Tuesday": "Cardio",
                    "Wednesday": "Rest",
                    "Thursday": "Strength",
                    "Friday": "Cardio",
                    "Saturday": "Flexibility",
                    "Sunday": "Rest"
                }
            }
            
        adapted = template.copy()
        structure = template.get("structure", {})
        
        if preferred_types is None:
            preferred_types = []
            
        # Adjust workout frequency based on fitness level
        if fitness_level == "Beginner":
            rest_days = [day for day, type_ in structure.items() if type_ == "Rest"]
            if len(rest_days) < 2:
                structure["Wednesday"] = "Rest"  # Add mid-week rest
        elif fitness_level == "Advanced":
            # Reduce rest days for advanced users
            rest_days = [day for day, type_ in structure.items() if type_ == "Rest"]
            if len(rest_days) > 1:
                for day in rest_days[:-1]:  # Keep at least one rest day
                    structure[day] = "Active Recovery"
                
        # Incorporate preferred workout types
        for day, workout_type in structure.items():
            if workout_type not in ["Rest", "Active Recovery"]:
                if "HIIT" in preferred_types and day in ["Tuesday", "Thursday"]:
                    structure[day] = "HIIT"
                elif "Strength" in preferred_types and day in ["Monday", "Friday"]:
                    structure[day] = "Strength"
                elif "Core" in preferred_types and workout_type == "Strength":
                    structure[day] = "Core"
                        
        adapted["structure"] = structure
        return adapted

    def generate_workout_plan(self, user: UserProfile, last_workout: Dict[str, Any] = None) -> WorkoutPlan:
        """Generate personalized workout plan for user
        
        Args:
            user: UserProfile object with user preferences and attributes
            last_workout: Dictionary containing the last workout details. Required before generating a new plan.
            
        Raises:
            ValueError: If last_workout is not provided
        """
        if last_workout is None:
            raise ValueError("Must specify last workout before generating a new plan")
            
        # Add last workout to past_workouts if not empty
        if not hasattr(user, 'past_workouts'):
            user.past_workouts = []
        user.past_workouts.append(last_workout)
            
        try:
            # Get user attributes with defaults
            injuries = getattr(user, 'injuries', [])
            equipment = getattr(user, 'equipment', [])
            preferred_workouts = getattr(user, 'preferred_workouts', [])
            fitness_level = getattr(user, 'fitness_level', "Beginner")
            goal = getattr(user, 'goal', "General Fitness")
            
            # Step 1: Filter exercises by safety rules and equipment
            safe_exercises = self._filter_exercises_by_injury(self.exercises, injuries)
            available_exercises = self._filter_exercises_by_equipment(safe_exercises, equipment)
            
            if not available_exercises:
                # Fallback to bodyweight exercises if no equipment matches
                available_exercises = [ex for ex in self.exercises if not ex.get('equipment_needed')]
            
            # Step 2: Apply user preferences and consider past workouts
            preferred_exercises = self._apply_user_preferences(
                available_exercises,
                preferred_workouts,
                fitness_level,
                getattr(user, 'past_workouts', [])
            )
            
            # Step 3: Categorize and balance exercises
            categorized_exercises = self._categorize_exercises(preferred_exercises)
            balanced_exercises = self._balance_muscle_groups(categorized_exercises)
            
            # Step 4: Get personalized template based on goal and preferences
            template = self._get_workout_template(goal)
            adapted_template = self._adapt_template_to_preferences(
                template,
                preferred_workouts,
                fitness_level
            )
        except AttributeError as e:
            print(f"Warning: Missing user attribute - {str(e)}")
            # Use defaults if attributes are missing
            template = self._get_workout_template("General Fitness")
            balanced_exercises = self._categorize_exercises(self.exercises)
        except Exception as e:
            print(f"Error generating workout plan: {str(e)}")
            raise
        
        # Step 5: Generate progressive parameters
        workout_params = self._generate_progressive_parameters(
            user.fitness_level,
            user.goal
        )
        
        # Step 6: Create weekly plan with variety and progression
        weekly_plan = self._generate_weekly_plan(
            balanced_exercises,
            adapted_template,
            workout_params,
            user.injuries
        )

        return WorkoutPlan(
            user_id=user.user_id,
            week_number=1,
            days=weekly_plan
        )

    def _generate_weekly_plan(self, exercises_by_type: Dict[str, List[Dict]],
                              template: Dict[str, Any],
                              params: Dict[str, Any],
                              injuries: List[str]) -> Dict[str, Dict[str, Any]]:
        """Generate a 7-day workout plan"""
        plan = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_schedule = self._create_day_schedule(template)

        for i, day in enumerate(days):
            workout_type = day_schedule[i] if i < len(day_schedule) else "Rest"

            if workout_type == "Rest":
                plan[day] = {"type": "Rest", "exercises": []}
            elif workout_type == "Active Recovery":
                plan[day] = {"type": "Active Recovery", "exercises": []}
            else:
                # Get exercises for this workout type
                available_for_type = exercises_by_type.get(workout_type, [])
                selected_exercises = self._select_exercises(available_for_type, workout_type, params, injuries)

                plan[day] = {
                    "type": workout_type,
                    "exercises": selected_exercises
                }

        return plan

    def _create_day_schedule(self, template: Dict[str, Any]) -> List[str]:
        """Create workout schedule for the week"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        structure = template.get("structure", {})
        
        # If it's a daily schedule, use it directly
        if any(day in structure for day in days):
            return [structure.get(day, "Rest") for day in days]
            
        # Otherwise, create a schedule from the workout type counts
        schedule = []
        for workout_type, count in structure.items():
            if isinstance(count, int):
                schedule.extend([workout_type] * count)
                
        # Fill remaining days
        remaining_days = 7 - len(schedule)
        if remaining_days > 0:
            schedule.extend(["Rest"] * remaining_days)

        # Ensure proper distribution (max 2 consecutive workout days)
        return self._optimize_schedule(schedule)

    def _optimize_schedule(self, schedule: List[str]) -> List[str]:
        """Optimize workout schedule to avoid consecutive intense workouts"""
        optimized = []
        rest_added = 0

        for i, workout in enumerate(schedule):
            optimized.append(workout)
            # Add rest day after 2 consecutive workouts (except for light workouts)
            if (i + 1 - rest_added) % 3 == 0 and workout not in ["Flexibility", "Mobility"]:
                optimized.append("Rest")
                rest_added += 1

        # Trim to 7 days if needed
        return optimized[:7]

    def _select_exercises(self, available_exercises: List[Dict],
                          workout_type: str,
                          params: Dict[str, Any],
                          injuries: List[str]) -> List[Dict[str, Any]]:
        """Select appropriate exercises for workout type"""
        if not available_exercises:
            return []

        # Map workout types to exercise types
        type_mapping = {
            "Strength": ["Strength", "Resistance"],
            "HIIT": ["HIIT", "Cardio"],
            "Cardio": ["Cardio", "HIIT"],
            "Core": ["Strength"],  # Core exercises are usually strength-based
            "Flexibility": ["Flexibility", "Mobility"],
            "Mobility": ["Mobility", "Flexibility"]
        }
        
        valid_types = type_mapping.get(workout_type, [workout_type])
        
        # Filter exercises by mapped types and ensure they're in the right format
        type_exercises = []
        for ex in available_exercises:
            ex_type = ex.get("exercise_type", "")
            if isinstance(ex_type, str) and ex_type.lower() in [t.lower() for t in valid_types]:
                # For Core workouts, also check muscle groups
                if workout_type == "Core" and "Core" not in ex.get("muscle_groups", []):
                    continue
                type_exercises.append(ex)
        
        if not type_exercises:
            print(f"No exercises found for type: {workout_type}")
            return []

        # Select 2-3 exercises randomly
        import random
        num_exercises = min(random.randint(2, 3), len(type_exercises))
        selected = random.sample(type_exercises, num_exercises)

        # Add parameters to each exercise
        enhanced_exercises = []
        for exercise in selected:
            enhanced_exercise = exercise.copy()
            # Use exercise-specific params if available, otherwise use defaults
            enhanced_exercise.update({
                "sets": exercise.get("sets", params.get("sets", 3)),
                "reps": exercise.get("reps", params.get("reps", 12)),
                "rest_period": exercise.get("rest_period", params.get("rest", "60s")),
                "notes": self._generate_exercise_notes(exercise, injuries)
            })
            enhanced_exercises.append(enhanced_exercise)

        return enhanced_exercises

    def _generate_exercise_notes(self, exercise: Dict[str, Any], injuries: List[str]) -> str:
        """Generate safety notes for exercises based on injuries"""
        notes = []

        # Check for injury-specific notes
        for injury in injuries:
            if injury in exercise.get("injury_restrictions", []):
                notes.append(f"Alternative: {', '.join(exercise.get('alternatives', ['None']))}")

        # Add general safety notes
        if exercise.get("intensity") == "High":
            notes.append("Monitor form carefully")

        return "; ".join(notes) if notes else "Perform with proper form"


# Example usage
if __name__ == "__main__":
    recommender = WorkoutRecommender()
    print("Workout Recommender initialized successfully!")