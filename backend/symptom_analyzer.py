# backend/symptom_analyzer.py

from ml.predict_disease import predict_disease


def analyze_symptoms(user_data):
    """
    Uses ML model to predict diseases from symptoms.
    Returns ranked conditions.
    """

    symptoms = user_data["symptoms"]

    try:
        predictions = predict_disease(symptoms, top_k=5)

    except Exception as e:
        print("ML prediction error:", e)
        return []

    ranked_conditions = []

    for pred in predictions:
        ranked_conditions.append({
            "condition": pred["disease"],
            "match_score": pred["probability"]
        })

    return ranked_conditions