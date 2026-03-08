# backend/risk_engine.py

CRITICAL_SYMPTOMS = [
    "chest pain",
    "shortness of breath",
    "unconsciousness"
]

HIGH_RISK_CONDITIONS = [
    "heart disease",
    "diabetes",
    "asthma",
    "high blood pressure"
]


def evaluate_risk(user_data):
    """
    Evaluates personalized risk level.
    Returns structured risk assessment.
    """

    age = user_data["age"]
    severity = user_data["severity"]
    symptoms = user_data["symptoms"]
    existing_conditions = user_data["existing_conditions"]

    risk_score = severity
    flags = []

    # 1️⃣ Severity Based Risk
    if severity >= 9:
        return {
            "risk_level": "emergency",
            "risk_score": 10,
            "flags": ["Critical severity level"]
        }

    # 2️⃣ Critical Symptom Check
    for symptom in symptoms:
        if symptom in CRITICAL_SYMPTOMS:
            risk_score += 3
            flags.append(f"Critical symptom detected: {symptom}")

    # 3️⃣ Age Risk Factor
    if age >= 60:
        risk_score += 2
        flags.append("Senior age risk factor")

    if age <= 5:
        risk_score += 2
        flags.append("High child vulnerability")

    # 4️⃣ Existing Condition Risk
    for condition in existing_conditions:
        if condition in HIGH_RISK_CONDITIONS:
            risk_score += 2
            flags.append(f"Pre-existing condition: {condition}")

    # 5️⃣ Final Classification
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
        "risk_score": risk_score,
        "flags": flags
    }