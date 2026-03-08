# backend/symptom_analyzer.py

from collections import defaultdict

# Symptom → Possible Conditions Map
SYMPTOM_CONDITION_MAP = {
    "fever": ["viral infection", "flu", "covid-19"],
    "headache": ["migraine", "tension headache", "flu"],
    "cough": ["flu", "common cold", "bronchitis"],
    "sore throat": ["common cold", "flu"],
    "fatigue": ["anemia", "viral infection", "thyroid disorder"],
    "chest pain": ["heart disease", "anxiety", "acid reflux"],
    "shortness of breath": ["asthma", "heart disease", "covid-19"],
    "nausea": ["food poisoning", "gastritis", "migraine"],
    "vomiting": ["food poisoning", "stomach infection"],
    "dizziness": ["low blood pressure", "anemia", "dehydration"]
}


def analyze_symptoms(user_data):
    """
    Takes validated user_data.
    Returns ranked list of possible conditions.
    """

    selected_symptoms = user_data["symptoms"]

    condition_scores = defaultdict(int)

    # Score conditions based on symptom matches
    for symptom in selected_symptoms:
        if symptom in SYMPTOM_CONDITION_MAP:
            for condition in SYMPTOM_CONDITION_MAP[symptom]:
                condition_scores[condition] += 1

    if not condition_scores:
        return []

    # Sort by highest score
    ranked_conditions = sorted(
        condition_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Convert to structured list
    result = [
        {
            "condition": condition,
            "match_score": score
        }
        for condition, score in ranked_conditions
    ]

    return result