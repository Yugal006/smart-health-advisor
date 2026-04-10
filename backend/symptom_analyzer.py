# backend/symptom_analyzer.py

from ml.predict_disease import predict_disease

def analyze_symptoms(user_data, top_k=5):
    """
    Predict diseases from user symptoms using trained ML model.
    Returns ranked list with match scores.
    """
    # -----------------------------
    # 1. Extract symptoms from user input
    # -----------------------------
    raw_input = user_data.get("symptoms", [])
    if not raw_input:
        return [{"rank": 1, "condition": "Not clearly identified", "match_score": 0}]

    # -----------------------------
    # 2. Predict using ML model
    # -----------------------------
    try:
        predictions = predict_disease(raw_input, top_k=top_k)
    except Exception as e:
        print("Prediction error:", e)
        return [{"rank": 1, "condition": "Not clearly identified", "match_score": 0}]

    # -----------------------------
    # 3. Build ranked output
    # -----------------------------
    ranked_conditions = [
        {
            "rank": i + 1,
            "condition": pred["disease"],
            "confidence": pred["probability"]
        }
        for i, pred in enumerate(predictions)
    ]

    # Ensure fallback
    if not ranked_conditions:
        ranked_conditions.append({
            "rank": 1,
            "condition": "Not clearly identified",
            "match_score": 0
        })

    return ranked_conditions