# backend/medicine_engine.py

import csv
import os

# ---------------------------------------------------
# File Path
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDICATIONS_CSV_PATH = os.path.join(BASE_DIR, "data", "medical_dataset.csv")


# ---------------------------------------------------
# Allergy → Unsafe Medicines
# ---------------------------------------------------

ALLERGY_MEDICINE_CONFLICTS = {
    "nsaid": ["ibuprofen"],
    "paracetamol": ["paracetamol"],
    "antihistamine": ["cetirizine"]
}


# ---------------------------------------------------
# Load Condition → Medicines Mapping
# ---------------------------------------------------

def load_condition_medicine_map():

    condition_map = {}

    try:

        with open(MEDICATIONS_CSV_PATH, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                disease = row["Disease"].strip().lower()
                medication = row["Medication"].strip()
                recommendation = row["Recommendation"].strip()

                if medication:

                    medicines = [m.strip().lower() for m in medication.split(";")]

                else:
                    medicines = []

                condition_map[disease] = {
                    "medicines": medicines,
                    "recommendation": recommendation
                }

    except Exception as e:
        print("Error loading medication dataset:", e)

    return condition_map


# Load dataset once
CONDITION_MEDICINE_MAP = load_condition_medicine_map()


# ---------------------------------------------------
# Medicine Suggestion Logic
# ---------------------------------------------------

def suggest_medicines(ranked_conditions, user_data, risk_data):
    if not ranked_conditions:
        return {
            "recommended_medicines": [],
            "warnings": []
        }

    top_conditions = [c["condition"].lower() for c in ranked_conditions[:3]]

    medicines = []
    warnings = []
    allergies = []  # You can expand to take actual user allergies
    age = user_data.get("age", 0)
    risk_level = risk_data.get("risk_level", "low")

    for cond in top_conditions:
        data = CONDITION_MEDICINE_MAP.get(cond)
        if not data:
            warnings.append(f"No medicine data available for {cond}")
            continue

        # Doctor-required check
        if data["recommendation"].lower() == "doctor required":
            warnings.append(f"Doctor consultation required for {cond}")
            continue

        # Add safe medicines
        for med in data["medicines"]:
            if med not in medicines:
                # Example age restriction
                if age < 12 and med == "ibuprofen":
                    warnings.append("Ibuprofen avoided for children under 12")
                    continue
                medicines.append(med)

    # High risk override
    if risk_level in ["high", "emergency"]:
        warnings.append("High risk detected — consult doctor immediately")
        medicines = []

    return {
        "recommended_medicines": medicines,
        "warnings": warnings
    }