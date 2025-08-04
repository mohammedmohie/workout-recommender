
# 🏋️‍♂️ Workout Plan Recommender System

An AI-powered platform for trainers and individuals to generate personalized, injury-aware workout plans and export beautiful PDF reports. Built for flexibility, safety, and professional presentation.

---

## 🚀 Features
- **Personalized Recommendations:** Plans tailored to user goals, fitness level, injuries, and available equipment
- **Injury-Aware Filtering:** Exercises are filtered to avoid aggravating injuries
- **Equipment-Based Matching:** Only recommends exercises that can be performed with available equipment
- **Goal-Oriented Templates:** Supports weight loss, muscle gain, strength, endurance, and general fitness
- **Streamlit GUI:** Trainers can enter client details and instantly generate PDF reports
- **PDF Export:** Professionally formatted, ready to share or print
- **Safety-First Approach:** Ensures all recommendations are safe and effective

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **Streamlit** (GUI)
- **FPDF** (PDF generation)
- **Pandas, NumPy, Scikit-learn** (data handling, ML-ready)
- **Pydantic** (data validation)

---

## 📦 Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/yourusername/workout-recommender.git
cd workout-recommender
pip install -r requirements.txt
```

---

## 🖥️ Usage

### 1. Run the Streamlit Trainer GUI
```bash
streamlit run streamlit_app.py
```

### 2. Enter Client Details
- Name, Age, Gender
- Fitness Goal & Level
- Injuries
- Preferred Workouts
- Available Equipment

### 3. Generate & Download PDF Report
- Click **Generate Workout Plan**
- Preview the plan in the browser
- Download the PDF report for sharing or printing

### 4. Programmatic Access
- See `main.py` and `src/` for API usage and integration

---

## 📝 Example PDF Report
<img src="https://user-images.githubusercontent.com/yourusername/example-pdf-preview.png" width="600"/>

---

## 🤝 Contributing
Pull requests, feature suggestions, and bug reports are welcome! Please open an issue or submit a PR.

---

## 📄 License
This project is licensed under the MIT License.

---

## 📬 Contact
- GitHub Issues: [workout-recommender/issues](https://github.com/yourusername/workout-recommender/issues)
- Email: mohammedmohie04@gmail.com

## Features
- Personalized workout recommendations
- Injury-aware exercise filtering
- Equipment-based exercise matching
- Goal-oriented workout templates
- Safety-first approach

## Installation
```bash
pip install -r requirements.txt

## Streamlit Trainer GUI

Easily generate and export beautiful workout plans as PDF reports for your clients.

### How to Use
1. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
2. Enter client details in the sidebar:
   - Name, Age, Gender
   - Fitness Goal & Level
   - Injuries
   - Preferred Workouts
   - Available Equipment
3. Click **Generate Workout Plan**
4. Preview the plan in the browser
5. Download the PDF report for sharing or printing

### PDF Report
- Professionally formatted
- Includes all client and workout details
- Ready for trainers to share with clients

---
For advanced usage, see the code in `main.py` and `src/` for programmatic access.
