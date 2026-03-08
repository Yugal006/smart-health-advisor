# ml/predict_disease.py

import joblib
import numpy as np
import os


BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "disease_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "symptom_columns.pkl")


# Load model once
model = joblib.load(MODEL_PATH)
symptom_columns = joblib.load(FEATURE_PATH)


def symptoms_to_vector(user_symptoms):
    """
    Convert symptom list to model vector
    """

    vector = np.zeros(len(symptom_columns), dtype="int8")

    for symptom in user_symptoms:
        if symptom in symptom_columns:
            index = symptom_columns.index(symptom)
            vector[index] = 1

    return vector


def predict_disease(user_symptoms, top_k=3):
    """
    Predict disease probabilities
    """

    vector = symptoms_to_vector(user_symptoms)

    probabilities = model.predict_proba([vector])[0]

    top_indices = np.argsort(probabilities)[::-1][:top_k]

    results = []

    for idx in top_indices:
        results.append({
            "disease": model.classes_[idx],
            "probability": round(float(probabilities[idx]) * 100, 2)
        })

    return results