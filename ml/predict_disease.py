import joblib
import numpy as np
import os


# =====================================================
# 1. LOAD MODEL & SYMPTOM LIST
# =====================================================

MODEL_PATH = os.path.join("ml", "disease_model.pkl")
FEATURE_PATH = os.path.join("ml", "symptom_columns.pkl")

print("Loading ML model...")

model = joblib.load(MODEL_PATH)
symptom_columns = joblib.load(FEATURE_PATH)

print("Model loaded successfully")
print("Total symptoms in model:", len(symptom_columns))


# =====================================================
# 2. CONVERT SYMPTOMS TO VECTOR
# =====================================================

def symptoms_to_vector(user_symptoms):
    """
    Convert user symptom list into model input vector
    """

    vector = np.zeros(len(symptom_columns), dtype="int8")

    for symptom in user_symptoms:
        if symptom in symptom_columns:
            index = symptom_columns.index(symptom)
            vector[index] = 1

    return vector


# =====================================================
# 3. PREDICT DISEASE
# =====================================================

def predict_disease(user_symptoms, top_k=3):
    """
    Predict disease based on user symptoms
    """

    vector = symptoms_to_vector(user_symptoms)

    probabilities = model.predict_proba([vector])[0]

    top_indices = np.argsort(probabilities)[::-1][:top_k]

    results = []

    for idx in top_indices:
        disease = model.classes_[idx]
        probability = probabilities[idx]

        results.append({
            "disease": disease,
            "probability": round(float(probability) * 100, 2)
        })

    return results


# =====================================================
# 4. TEST (ONLY FOR DIRECT RUN)
# =====================================================

if __name__ == "__main__":

    test_symptoms = [
        "fever",
        "cough",
        "fatigue"
    ]

    print("\nTesting prediction...\n")

    predictions = predict_disease(test_symptoms)

    for i, pred in enumerate(predictions, 1):
        print(f"{i}. {pred['disease']} — {pred['probability']}%")