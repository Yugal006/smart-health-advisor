import csv
import os

# ----------------------------------
# LOAD DATASET (Condition Advice)
# ----------------------------------

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
    print("Error loading medical dataset:", e)


# ----------------------------------
# DOCTOR SPECIALIZATION MAP
# ----------------------------------

CONDITION_DOCTOR_MAP = {

    # General infections
    "common cold": "General Physician",
    "influenza": "General Physician",
    "viral fever": "General Physician",

    # Respiratory
    "bronchitis": "Pulmonologist",
    "pneumonia": "Pulmonologist",
    "asthma": "Pulmonologist",

    # Digestive
    "gastritis": "Gastroenterologist",
    "food poisoning": "Gastroenterologist",

    # Cardiac
    "heart attack": "Cardiologist",
    "angina": "Cardiologist",

    # Neurological
    "migraine": "Neurologist",
    "stroke": "Neurologist",

    # Mental health
    "anxiety": "Psychiatrist",
    "depression": "Psychiatrist",

    # Urinary
    "cystitis": "Urologist",
    "urinary tract infection": "Urologist",
    "kidney infection": "Urologist",

    # Bones
    "fracture": "Orthopedist",
    "arthritis": "Orthopedist",

    # Skin
    "dermatitis": "Dermatologist",
    "skin allergy": "Dermatologist",

    # ENT
    "sinusitis": "ENT Specialist",
    "ear infection": "ENT Specialist",
    "laryngitis": "ENT Specialist",

    # Eye
    "conjunctivitis": "Ophthalmologist"
}


# ----------------------------------
# KEYWORD BASED DOCTOR DETECTION
# ----------------------------------

SYMPTOM_DOCTOR_MAP = {

    "urination": "Urologist",
    "kidney": "Urologist",
    "urinary": "Urologist",

    "breathing": "Pulmonologist",
    "lung": "Pulmonologist",

    "heart": "Cardiologist",
    "chest pain": "Cardiologist",

    "skin": "Dermatologist",
    "rash": "Dermatologist",

    "eye": "Ophthalmologist",
    "vision": "Ophthalmologist",

    "ear": "ENT Specialist",
    "nose": "ENT Specialist",
    "throat": "ENT Specialist",

    "joint": "Orthopedist",
    "bone": "Orthopedist",

    "anxiety": "Psychiatrist",
    "depression": "Psychiatrist",

    "headache": "Neurologist",
    "seizure": "Neurologist"
}


# ----------------------------------
# SMART DOCTOR DETECTION
# ----------------------------------

def detect_doctor(top_condition, symptoms):

    condition = top_condition.lower()

    # 1️⃣ Exact disease match
    if condition in CONDITION_DOCTOR_MAP:
        return CONDITION_DOCTOR_MAP[condition]

    # 2️⃣ Keyword match in condition
    for key in SYMPTOM_DOCTOR_MAP:
        if key in condition:
            return SYMPTOM_DOCTOR_MAP[key]

    # 3️⃣ Keyword match in symptoms
    for s in symptoms:
        s = s.lower()

        for key in SYMPTOM_DOCTOR_MAP:
            if key in s:
                return SYMPTOM_DOCTOR_MAP[key]

    # Default
    return "General Physician"


# ----------------------------------
# URGENCY DECISION ENGINE
# ----------------------------------

def determine_urgency(risk_level, recommendation):

    risk_level = risk_level.lower()
    recommendation = recommendation.lower()

    if risk_level == "emergency":
        return "Immediate", "Seek emergency medical care immediately."

    if risk_level == "high":
        return "Consult doctor within 24 hours", "Medical consultation is strongly recommended."

    if risk_level == "moderate":
        return "Consult doctor within 24–48 hours", "Monitor symptoms and consult a doctor soon."

    if recommendation == "home care":
        return "Home care recommended", "Condition can usually be managed with rest and basic medication."

    return "Monitor symptoms", "Consult a doctor if symptoms worsen or persist."


# ----------------------------------
# MAIN APPOINTMENT RECOMMENDATION
# ----------------------------------

def recommend_appointment(ranked_conditions, risk_data, user_data=None):

    age = user_data.get("age", 0) if user_data else 0
    symptoms = user_data.get("symptoms", []) if user_data else []

    risk_level = risk_data.get("risk_level", "low")

    if not ranked_conditions:
        return {
            "doctor_type": "General Physician",
            "urgency": "Monitor symptoms",
            "message": "No specific condition identified. If symptoms persist, consult a doctor."
        }

    # ----------------------------
    # TOP CONDITION
    # ----------------------------

    top_condition = ranked_conditions[0]["condition"].lower()

    # ----------------------------
    # DOCTOR DETECTION
    # ----------------------------

    doctor = detect_doctor(top_condition, symptoms)

    # ----------------------------
    # AGE ADJUSTMENT
    # ----------------------------

    if age <= 16:
        doctor = "Pediatrician"

    elif age >= 65:
        doctor = "Geriatric Specialist"

    # ----------------------------
    # RECOMMENDATION TYPE
    # ----------------------------

    recommendation_type = CONDITION_RECOMMENDATION.get(
        top_condition,
        "Doctor Required"
    )

    # ----------------------------
    # URGENCY
    # ----------------------------

    urgency, message = determine_urgency(risk_level, recommendation_type)

    # ----------------------------
    # FINAL MESSAGE
    # ----------------------------

    final_message = f"{message} Possible condition detected: {top_condition.title()}."

    return {
        "doctor_type": doctor,
        "urgency": urgency,
        "message": final_message
    }