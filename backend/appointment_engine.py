# backend/appointment_engine.py

import csv
import os

# -------------------------------
# Load Condition → Recommendation
# -------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MED_CSV_PATH = os.path.join(BASE_DIR, "data", "medical_dataset.csv")

CONDITION_RECOMMENDATION = {}
try:
    with open(MED_CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            condition = row["Disease"].strip().lower()
            recommendation = row.get("Recommendation", "Doctor Required").strip()
            CONDITION_RECOMMENDATION[condition] = recommendation
except Exception as e:
    print("Error loading medical dataset for appointments:", e)


# -------------------------------
# Default Doctor Mapping
# -------------------------------

CONDITION_DOCTOR_MAP = {
    "flu": "General Physician",
    "viral infection": "General Physician",
    "migraine": "Neurologist",
    "tension headache": "General Physician",
    "common cold": "General Physician",
    "bronchitis": "Pulmonologist",
    "heart disease": "Cardiologist",
    "asthma": "Pulmonologist",
    "food poisoning": "Gastroenterologist",
    "gastritis": "Gastroenterologist",
    "anxiety": "Psychiatrist",
    "depression": "Psychiatrist",
    "pregnancy-related issue": "Gynecologist",
    "vaginitis": "Gynecologist",
    "fracture": "Orthopedist",
    "joint injury": "Orthopedist",
    "skin rash": "Dermatologist",
    "eye problem": "Ophthalmologist",
    "ear problem": "ENT Specialist"
}


# -------------------------------
# Smart Appointment Recommendation
# -------------------------------

def recommend_appointment(ranked_conditions, risk_data, user_data=None):
    """
    Determines doctor type, urgency, and personalized advice.
    """

    age = user_data.get("age", 0) if user_data else 0
    risk_level = risk_data.get("risk_level", "low")

    # Emergency override
    if risk_level == "emergency":
        return {
            "doctor_type": "Emergency Care",
            "urgency": "Immediate",
            "message": "Seek emergency medical care immediately."
        }

    if not ranked_conditions:
        return {
            "doctor_type": "General Physician",
            "urgency": "Monitor symptoms",
            "message": "No specific condition identified. Consult a doctor if symptoms persist or worsen."
        }

    # Pick top 1–2 conditions for doctor suggestion
    top_conditions = [c["condition"].lower() for c in ranked_conditions[:2]]

    # Determine doctor type
    doctor = "General Physician"
    for cond in top_conditions:
        if cond in CONDITION_DOCTOR_MAP:
            doctor = CONDITION_DOCTOR_MAP[cond]
            break

    # Age-based adjustments
    if age <= 16:
        doctor = "Pediatrician"
    elif age >= 65:
        doctor = "Geriatric Specialist"

    # Determine urgency & message
    top_condition = ranked_conditions[0]["condition"].lower()
    recommendation_type = CONDITION_RECOMMENDATION.get(top_condition, "Doctor Required")

    if recommendation_type.lower() == "doctor required":
        if risk_level in ["high", "moderate"]:
            urgency = "Consult doctor within 24-48 hours"
            message = f"Consult a doctor for {top_condition.title()} to ensure proper treatment."
        elif risk_level == "low":
            urgency = "Schedule appointment if symptoms persist"
            message = f"Monitor symptoms, but a doctor visit may be required for {top_condition.title()}."
        else:
            urgency = "Immediate medical attention"
            message = f"Seek urgent care for {top_condition.title()}!"
    else:
        if risk_level in ["moderate", "high"]:
            urgency = "Consult doctor if condition worsens"
            message = f"You can manage {top_condition.title()} at home, but monitor for worsening symptoms."
        else:
            urgency = "Home care recommended"
            message = f"{top_condition.title()} can be managed at home using available medicines."

    return {
        "doctor_type": doctor,
        "urgency": urgency,
        "message": message
    }