# backend/medicine_engine.py

# Condition → Suggested Medicines
CONDITION_MEDICINE_MAP = {
    "flu": ["paracetamol", "ibuprofen"],
    "viral infection": ["paracetamol"],
    "migraine": ["ibuprofen"],
    "tension headache": ["paracetamol"],
    "common cold": ["cetirizine", "paracetamol"],
    "bronchitis": ["cough syrup"],
    "heart disease": ["consult specialist only"],
    "asthma": ["inhaler"],
    "food poisoning": ["oral rehydration salts"],
    "gastritis": ["antacid"]
}

# Allergy → Unsafe Medicines
ALLERGY_MEDICINE_CONFLICTS = {
    "nsaid": ["ibuprofen"],
    "paracetamol": ["paracetamol"],
    "antihistamine": ["cetirizine"]
}


def suggest_medicines(ranked_conditions, user_data, risk_data):
    """
    Suggest medicines based on top condition.
    Applies allergy and risk filtering.
    """

    if not ranked_conditions:
        return {
            "recommended_medicines": [],
            "warnings": []
        }

    top_condition = ranked_conditions[0]["condition"]
    suggested = CONDITION_MEDICINE_MAP.get(top_condition, [])

    allergies = user_data["allergies"]
    age = user_data["age"]
    risk_level = risk_data["risk_level"]

    safe_medicines = []
    warnings = []

    for medicine in suggested:

        # 1️⃣ Allergy Filter
        unsafe = False
        for allergy in allergies:
            if allergy in ALLERGY_MEDICINE_CONFLICTS:
                if medicine in ALLERGY_MEDICINE_CONFLICTS[allergy]:
                    unsafe = True
                    warnings.append(f"{medicine} removed due to {allergy} allergy")

        if unsafe:
            continue

        # 2️⃣ Age Restriction (basic rule example)
        if age < 12 and medicine == "ibuprofen":
            warnings.append("Ibuprofen avoided for children under 12")
            continue

        # 3️⃣ High Risk Override
        if risk_level in ["high", "emergency"]:
            warnings.append("High risk detected – medicine suggestion limited")
            return []

        safe_medicines.append(medicine)

    return {
        "recommended_medicines": safe_medicines,
        "warnings": warnings
    }