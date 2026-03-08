import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# =====================================================
# 1. CONFIGURATION
# =====================================================

DATA_PATH = "data/Final_Augmented_dataset_Diseases_and_Symptoms.csv"
MODEL_PATH = "ml/disease_model.pkl"
FEATURE_PATH = "ml/symptom_columns.pkl"


# =====================================================
# 2. LOAD DATASET
# =====================================================

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Original Dataset Shape:", df.shape)


# =====================================================
# 3. REMOVE RARE DISEASES (only 1 sample)
# =====================================================

disease_counts = df.iloc[:, 0].value_counts()

valid_diseases = disease_counts[disease_counts > 1].index

df = df[df.iloc[:, 0].isin(valid_diseases)]

print("Dataset after removing rare diseases:", df.shape)


# =====================================================
# 4. PREPARE FEATURES & TARGET
# =====================================================

# disease column
y = df.iloc[:, 0]

# symptom columns
X = df.iloc[:, 1:]

# reduce memory (values are 0/1)
X = X.astype("int8")

print("\nFeature Matrix Shape:", X.shape)
print("Target Shape:", y.shape)

# save symptom column names
symptom_columns = X.columns.tolist()


# =====================================================
# 5. TRAIN / TEST SPLIT
# =====================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
    shuffle=True
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =====================================================
# 6. TRAIN MODEL
# =====================================================

print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=80,
    max_depth=25,
    min_samples_split=5,
    n_jobs=2,
    random_state=42
)

model.fit(X_train, y_train)

print("Model training completed")


# =====================================================
# 7. MODEL EVALUATION
# =====================================================

print("\nEvaluating model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# =====================================================
# 8. SAVE MODEL
# =====================================================

print("\nSaving model...")

os.makedirs("ml", exist_ok=True)

joblib.dump(model, MODEL_PATH)
joblib.dump(symptom_columns, FEATURE_PATH)

print("Model saved at:", MODEL_PATH)
print("Symptom columns saved at:", FEATURE_PATH)


# =====================================================
# 9. TRAINING COMPLETE
# =====================================================

print("\nML training pipeline completed successfully 🚀")