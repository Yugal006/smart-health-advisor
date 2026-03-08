import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------
# 1. LOAD DATASET
# -----------------------------

DATA_PATH = "data/Final_Augmented_dataset_Diseases_and_Symptoms.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
print("Dataset Shape:", df.shape)
# print(df.columns)


# -----------------------------
# 2. PREPARE FEATURES & TARGET
# -----------------------------

# disease column
y = df.iloc[:, 0]

# symptom columns
X = df.iloc[:, 1:]

print("Features:", X.shape)
print("Target:", y.shape)


# -----------------------------
# 3. TRAIN / TEST SPLIT
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# 4. TRAIN MODEL
# -----------------------------

print("Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=50,
    max_depth=20,
    random_state=42,
    n_jobs=1
)

model.fit(X_train, y_train)

print("Training completed.")

# -----------------------------
# 5. MODEL EVALUATION
# -----------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# -----------------------------
# 6. SAVE MODEL
# -----------------------------

MODEL_PATH = "ml/disease_model.pkl"

joblib.dump(model, MODEL_PATH)

print("\nModel saved at:", MODEL_PATH)