import pandas as pd
import joblib

df1 = pd.read_csv("data/Final_Augmented_dataset_Diseases_and_Symptoms.csv")
df2 = pd.read_csv("data/expanded_symptoms.csv")

# Ensure column name
df1.rename(columns={df1.columns[0]: "disease"}, inplace=True)
df2.rename(columns={df2.columns[0]: "disease"}, inplace=True)

dataset = pd.concat([df1, df2], ignore_index=True)
dataset = dataset.dropna(subset=["disease"])

disease_symptom_map = {}
symptom_disease_map = {}

for _, row in dataset.iterrows():

    # FIX: skip rows with missing disease
    if pd.isna(row["disease"]):
        continue

    disease = str(row["disease"]).strip().lower()

    symptoms = {
        col for col in dataset.columns[1:]
        if row[col] == 1
    }

    disease_symptom_map[disease] = symptoms

    for s in symptoms:
        symptom_disease_map.setdefault(s, set()).add(disease)

joblib.dump(disease_symptom_map, "ml/disease_symptom_map.pkl")
joblib.dump(symptom_disease_map, "ml/symptom_disease_map.pkl")

print("Index built successfully")