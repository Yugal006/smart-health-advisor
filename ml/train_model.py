# ml/train_model.py

import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# =====================================================
# 1. CONFIGURATION
# =====================================================

DATASET_1 = "data/Final_Augmented_dataset_Diseases_and_Symptoms.csv"
DATASET_2 = "data/expanded_symptoms.csv"

MODEL_PATH = "ml/disease_model.pkl"
FEATURE_PATH = "ml/symptom_columns.pkl"

# Compression level for joblib (1–9)
COMPRESSION_LEVEL = 3  # can increase to 6 or 9 for smaller files


# =====================================================
# 2. LOAD DATASETS
# =====================================================

print("\nLoading datasets...")

df1 = pd.read_csv(DATASET_1)
df2 = pd.read_csv(DATASET_2)

print("Dataset 1 shape:", df1.shape)
print("Dataset 2 shape:", df2.shape)


# =====================================================
# ALIGN SYMPTOM COLUMNS
# =====================================================

print("\nAligning symptom columns...")

df1.rename(columns={df1.columns[0]: "disease"}, inplace=True)
df2.rename(columns={df2.columns[0]: "disease"}, inplace=True)

symptoms1 = set(df1.columns) - {"disease"}
symptoms2 = set(df2.columns) - {"disease"}

all_symptoms = symptoms1.union(symptoms2)

print("Total symptoms after merge:", len(all_symptoms))

ordered_columns = ["disease"] + sorted(all_symptoms)

df1 = df1.reindex(columns=ordered_columns, fill_value=0)
df2 = df2.reindex(columns=ordered_columns, fill_value=0)


# =====================================================
# 4. MERGE DATASETS
# =====================================================

print("\nMerging datasets...")

df = pd.concat([df1, df2], ignore_index=True)

print("Merged dataset shape:", df.shape)


# =====================================================
# 5. REMOVE RARE DISEASES
# =====================================================

print("\nRemoving rare diseases...")

disease_counts = df["disease"].value_counts()
valid_diseases = disease_counts[disease_counts > 1].index
df = df[df["disease"].isin(valid_diseases)]

print("Dataset after filtering:", df.shape)


# =====================================================
# 6. PREPARE FEATURES
# =====================================================

y = df["disease"]
X = df.drop("disease", axis=1)
X = X.astype("int8")

symptom_columns = X.columns.tolist()

print("\nFeature matrix:", X.shape)


# =====================================================
# 7. TRAIN TEST SPLIT
# =====================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =====================================================
# 8. TRAIN MODEL
# =====================================================

print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=120,
    max_depth=25,
    min_samples_split=5,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

print("Model training completed")


# =====================================================
# 9. EVALUATE MODEL
# =====================================================

print("\nEvaluating model...")

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# =====================================================
# 10. SAVE MODEL (COMPRESSED)
# =====================================================

print("\nSaving model with compression...")

os.makedirs("ml", exist_ok=True)

joblib.dump(model, MODEL_PATH, compress=COMPRESSION_LEVEL)
joblib.dump(symptom_columns, FEATURE_PATH, compress=COMPRESSION_LEVEL)

print("Model saved to:", MODEL_PATH)
print("Symptom columns saved to:", FEATURE_PATH)

print("\nTraining pipeline completed successfully 🚀")