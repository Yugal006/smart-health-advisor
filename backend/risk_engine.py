# backend/risk_engine.py
from ml.predict_disease import normalize_symptom
import csv
import os

# ---------------------------------------------------
# Load Symptom Severity Dataset
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SEVERITY_PATH = os.path.join(BASE_DIR, "data", "Symptom-severity.csv")

symptom_severity = {}

try:
    with open(SEVERITY_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symptom = row["Disease"].strip().lower().replace(" ", "_")
            try:
                severity = int(row["weight"])
                symptom_severity[symptom] = severity
            except ValueError:
                continue
except Exception as e:
    print("Error loading symptom severity dataset:", e)


# ---------------------------------------------------
# Risk Constants
# ---------------------------------------------------

CRITICAL_SYMPTOMS = [
    "chest_pain",
    "shortness_of_breath",
    "unconsciousness"
]

HIGH_RISK_CONDITIONS = [
    "heart disease",
    "diabetes",
    "asthma",
    "high blood pressure"
]


# ---------------------------------------------------
# Calculate Symptom Severity Score
# ---------------------------------------------------

def calculate_symptom_severity(symptoms):

    if not symptoms:
        return 0

    total = 0
    count = 0

    for symptom in symptoms:

        symptom = symptom.strip().lower().replace(" ", "_")

        if symptom in symptom_severity:
            total += symptom_severity[symptom]
            count += 1

    if count == 0:
        return 0

    return total / count


# ---------------------------------------------------
# Main Risk Evaluation
# ---------------------------------------------------

def evaluate_risk(user_data):
    """
    Evaluates personalized risk level.
    Returns structured risk assessment.
    """
    age = user_data.get("age", 0)
    severity = user_data.get("severity", 0)
    symptoms = user_data.get("symptoms", [])
    existing_conditions = user_data.get("existing_conditions", [])
    predicted_condition = user_data.get("predicted_condition", "")

    flags = []

    # ---------------------------------------------------
    # Dataset Symptom Severity
    # ---------------------------------------------------

    dataset_severity = calculate_symptom_severity(symptoms)

    risk_score = severity + dataset_severity

    # ---------------------------------------------------
    # Emergency Severity Check
    # ---------------------------------------------------
    if predicted_condition in HIGH_RISK_CONDITIONS:
        risk_score += 3
        flags.append("High-risk predicted condition")

    if severity >= 9:
        return {
            "risk_level": "emergency",
            "risk_score": 10,
            "flags": ["Critical severity level"]
        }

    # ---------------------------------------------------
    # Critical Symptoms
    # ---------------------------------------------------

    for symptom in symptoms:

        symptom = symptom.strip().lower().replace(" ", "_")

        if symptom in CRITICAL_SYMPTOMS:
            risk_score += 3
            flags.append(f"Critical symptom detected: {symptom.replace('_',' ')}")

    # ---------------------------------------------------
    # Age Risk
    # ---------------------------------------------------

    if age >= 60:
        risk_score += 2
        flags.append("Senior age risk factor")

    if age <= 5:
        risk_score += 2
        flags.append("High child vulnerability")

    # ---------------------------------------------------
    # Existing Conditions
    # ---------------------------------------------------

    for condition in existing_conditions:

        condition = condition.lower()

        if condition in HIGH_RISK_CONDITIONS:
            risk_score += 2
            flags.append(f"Pre-existing condition: {condition}")

    # ---------------------------------------------------
    # Final Risk Classification
    # ---------------------------------------------------

    if risk_score <= 3:
        risk_level = "low"

    elif risk_score <= 6:
        risk_level = "moderate"

    elif risk_score <= 8:
        risk_level = "high"

    else:
        risk_level = "emergency"

    return {
        "risk_level": risk_level,
        "risk_score": round(risk_score, 2),
        "flags": flags
    }