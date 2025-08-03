"""
Streamlit GUI for Workout Recommender System
"""
import streamlit as st
from fpdf import FPDF
import json
from datetime import datetime
import os

from src.recommender import WorkoutRecommender
from src.data_models import UserProfile

def create_pdf(user, workout_plan):
    pdf = FPDF()
    pdf.add_page()
    
    # Enable utf-8 support
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Set up fonts
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(31, 41, 55)
    
    # Header
    pdf.cell(0, 20, "Personalized Workout Plan", align="C", ln=True)
    
    # User Information
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Profile: {user.name}", ln=True)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Goal: {user.goal} | Fitness Level: {user.fitness_level}", ln=True)
    pdf.cell(0, 10, f"Age: {user.age} | Gender: {user.gender}", ln=True)
    
    if user.injuries:
        pdf.cell(0, 10, f"Injuries: {', '.join(user.injuries)}", ln=True)
    
    pdf.cell(0, 10, f"Available Equipment: {', '.join(user.equipment)}", ln=True)
    pdf.ln(10)
    
    # Weekly Plan
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Weekly Workout Schedule", ln=True)
    pdf.ln(5)
    
    for day, workout in workout_plan.days.items():
        # Day header
        pdf.set_font("Arial", "B", 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, day.upper(), ln=True, fill=True)
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Type: {workout['type']}", ln=True)
        
        if workout['exercises']:
            for i, exercise in enumerate(workout['exercises'], 1):
                pdf.cell(0, 10, f"{i}. {exercise['name']}", ln=True)
                if 'sets' in exercise:
                    pdf.cell(0, 10, 
                        f"   Sets: {exercise['sets']} | Reps: {exercise['reps']} | " 
                        f"Rest: {exercise['rest_period']}", ln=True)
                if exercise.get('notes'):
                    pdf.cell(0, 10, f"   Note: {exercise['notes']}", ln=True)
        else:
            if workout['type'] == "Rest":
                pdf.cell(0, 10, "   Complete rest day - focus on recovery", ln=True)
            elif workout['type'] == "Active Recovery":
                pdf.cell(0, 10, "   Light stretching or yoga", ln=True)
        pdf.ln(5)
    
    # Footer
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    
    return pdf

def main():
    st.set_page_config(
        page_title="Workout Plan Generator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1c1f 0%, #2d3436 100%);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        }
        .stSelectbox, .stMultiSelect {
            background-color: #2d3436;
        }
        .sidebar .stTextInput>div>div>input {
            background-color: #2d3436;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header with custom styling
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏋️ Workout Plan Generator</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for user input
    with st.sidebar:
        st.markdown("<h3 style='color: #4CAF50;'>Enter User Details</h3>", unsafe_allow_html=True)
        
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=16, max_value=90, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        goal = st.selectbox("Fitness Goal", [
            "Weight Loss",
            "Muscle Gain",
            "Strength",
            "Endurance",
            "General Fitness"
        ])
        
        fitness_level = st.selectbox("Fitness Level", [
            "Beginner",
            "Intermediate",
            "Advanced"
        ])
        
        injuries = st.multiselect("Injuries (if any)", [
            "None",
            "Knee Injury",
            "Back Pain",
            "Shoulder Injury",
            "Ankle Sprain",
            "Hip Pain",
            "Wrist Pain"
        ])
        
        preferred_workouts = st.multiselect("Preferred Workout Types", [
            "Strength Training",
            "Cardio",
            "HIIT",
            "Yoga",
            "Bodyweight",
            "Pilates"
        ])
        
        equipment = st.multiselect("Available Equipment", [
            "Dumbbells",
            "Resistance Bands",
            "Barbell",
            "Kettlebells",
            "Pull-up Bar",
            "Yoga Mat",
            "Stationary Bike",
            "Treadmill",
            "None"
        ])
        
        # Previous Workout Section
        st.markdown("<h3 style='color: #4CAF50;'>Previous Workout Details</h3>", unsafe_allow_html=True)
        
        has_previous_workout = st.checkbox("I have completed a previous workout")
        
        previous_workout = None
        if has_previous_workout:
            prev_workout_type = st.selectbox("Previous Workout Type", [
                "Strength Training",
                "Cardio",
                "HIIT",
                "Yoga",
                "Bodyweight",
                "Pilates"
            ])
            
            satisfaction = st.slider(
                "How satisfied were you with the workout?",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Not satisfied, 5 = Very satisfied"
            )
            
            intensity = st.selectbox("How intense was the workout?", [
                "Low",
                "Moderate",
                "High"
            ])
            
            previous_workout = {
                'completed': True,
                'workout_type': prev_workout_type,
                'satisfaction': satisfaction,
                'intensity': intensity
            }
        else:
            # Default first workout
            previous_workout = {
                'completed': True,
                'workout_type': 'General Fitness',
                'satisfaction': 3,
                'intensity': 'Moderate'
            }
    
    # Main content
    if st.sidebar.button("Generate Workout Plan", key="generate_btn"):
        if not all([name, goal, fitness_level, preferred_workouts, equipment]):
            st.error("Please fill in all required fields!")
            return
        
        # Create user profile
        user = UserProfile(
            user_id=f"U{datetime.now().strftime('%Y%m%d%H%M')}",
            name=name,
            age=age,
            gender=gender,
            goal=goal,
            fitness_level=fitness_level,
            injuries=[inj for inj in injuries if inj != "None"],
            preferred_workouts=preferred_workouts,
            equipment=equipment,
            past_workouts=[]  # Could be added as a feature later
        )
        
        # Generate workout plan
        recommender = WorkoutRecommender()
        workout_plan = recommender.generate_workout_plan(user, previous_workout)
        
        # Store the current workout for next time
        st.session_state['last_workout'] = {
            'completed': True,
            'workout_type': workout_plan.days['Monday']['type'],  # Use first day's type
            'satisfaction': 3,  # Default satisfaction
            'intensity': 'Moderate'  # Default intensity
        }
        
        # Create PDF in memory
        pdf = create_pdf(user, workout_plan)
        pdf_filename = f"workout_plan_{user.name.lower().replace(' ', '_')}.pdf"
        
        # Generate PDF bytes with proper encoding
        from io import BytesIO
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_buffer = BytesIO(pdf_output)
        
        # Display success message and download button
        st.success("Workout plan generated successfully!")
        
        st.download_button(
            label="Download Workout Plan (PDF)",
            data=pdf_buffer,
            file_name=pdf_filename,
                mime="application/pdf"
            )
        
        # Display preview
        st.subheader("Preview")
        for day, workout in workout_plan.days.items():
            with st.expander(f"{day.upper()} - {workout['type']}", expanded=True):
                if workout['exercises']:
                    for i, exercise in enumerate(workout['exercises'], 1):
                        st.write(f"{i}. {exercise['name']}")
                        sets = exercise.get('sets')
                        reps = exercise.get('reps')
                        rest = exercise.get('rest_period')
                        if sets and reps and rest:
                            st.write(f"   Sets: {sets} | Reps: {reps} | Rest: {rest}")
                        else:
                            st.write("   No set/rep/rest info available.")
                        if exercise.get('notes'):
                            st.write(f"   Note: {exercise['notes']}")
                else:
                    if workout['type'] == "Rest":
                        st.write("Complete rest day - focus on recovery")
                    elif workout['type'] == "Active Recovery":
                        st.write("Light stretching or yoga")
                    else:
                        st.write("No exercises assigned for this day.")

if __name__ == "__main__":
    main()
