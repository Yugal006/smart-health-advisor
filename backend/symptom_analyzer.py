# backend/symptom_analyzer.py

from ml.predict_disease import predict_disease
import re

def analyze_symptoms(user_data):
    """
    Uses ML model to predict diseases from symptoms.
    Returns ranked possible conditions.
    """

    # Raw input from frontend
    raw_input = user_data.get("symptoms", [])

    # Normalize and split concatenated symptoms
    symptoms = []
    for s in raw_input:
        # replace commas with space
        s_clean = s.replace(",", " ").lower()
        # split on spaces
        tokens = s_clean.split()
        # optional: further split concatenated words using regex for letters+digits
        for t in tokens:
            # remove non-alphabetic chars, just in case
            t = re.sub(r'[^a-z_]', '', t)
            if t:
                symptoms.append(t)

    if not symptoms:
        return []

    try:
        # Predict top 5 conditions
        predictions = predict_disease(symptoms, top_k=5)

    except Exception as e:
        print("ML prediction error:", e)
        return []

    ranked_conditions = [
        {"rank": i+1, "condition": pred["disease"], "match_score": pred["probability"]}
        for i, pred in enumerate(predictions)
    ]

    return ranked_conditions