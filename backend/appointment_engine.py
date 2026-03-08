# backend/appointment_engine.py

CONDITION_DOCTOR_MAP = {
    "flu": "General Physician",
    "viral infection": "General Physician",
    "migraine": "Neurologist",
    "tension headache": "General Physician",
    "common cold": "General Physician",
    "bronchitis": "Pulmonologist",
    "heart disease": "Cardiologist",
    "asthma": "Pulmonologist",
    "food poisoning": "General Physician",
    "gastritis": "Gastroenterologist"
}


def recommend_appointment(ranked_conditions, risk_data):
    """
    Determines doctor type and urgency level.
    """

    if risk_data["risk_level"] == "emergency":
        return {
            "doctor_type": "Emergency Care",
            "urgency": "Immediate medical attention required",
            "message": "Please visit the nearest emergency center immediately."
        }

    if not ranked_conditions:
        return {
            "doctor_type": "General Physician",
            "urgency": "Consult if symptoms persist",
            "message": "Monitor symptoms and consult a doctor if condition worsens."
        }

    top_condition = ranked_conditions[0]["condition"]
    doctor = CONDITION_DOCTOR_MAP.get(top_condition, "General Physician")

    risk_level = risk_data["risk_level"]

    if risk_level == "low":
        urgency = "Home care recommended"
        message = "Manage symptoms at home. Visit doctor if no improvement in 2-3 days."

    elif risk_level == "moderate":
        urgency = "Schedule appointment within 48 hours"
        message = "Consult a doctor if symptoms do not improve."

    else:  # high risk
        urgency = "Consult doctor within 24 hours"
        message = "Early medical consultation is strongly recommended."

    return {
        "doctor_type": doctor,
        "urgency": urgency,
        "message": message
    }