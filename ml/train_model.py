# ml/train_model.py

import pandas as pd
import joblib
import os
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from xgboost import XGBClassifier

 
# =====================================================
# 1. CONFIGURATION
# =====================================================

DATASET_1 = "data/Final_Augmented_dataset_Diseases_and_Symptoms.csv"
DATASET_2 = "data/expanded_symptoms.csv"

MODEL_PATH = "ml/disease_model.pkl"
FEATURE_PATH = "ml/symptom_columns.pkl"
LABEL_ENCODER_PATH = "ml/disease_label_encoder.pkl"
METRICS_PATH = "ml/model_metrics.json"

COMPRESSION_LEVEL = 3


# =====================================================
# 2. LOAD DATASETS
# =====================================================

print("\nLoading datasets...")

df1 = pd.read_csv(DATASET_1)
df2 = pd.read_csv(DATASET_2)

print("Dataset 1 shape:", df1.shape)
print("Dataset 2 shape:", df2.shape)


# =====================================================
# 3. INITIAL DATA QUALITY CHECK
# =====================================================

print("\nChecking data quality...")

dataset1_duplicates = int(df1.duplicated().sum())
dataset2_duplicates = int(df2.duplicated().sum())

dataset1_missing = int(df1.isna().sum().sum())
dataset2_missing = int(df2.isna().sum().sum())

print("Dataset 1 duplicate rows:", dataset1_duplicates)
print("Dataset 2 duplicate rows:", dataset2_duplicates)

print("Dataset 1 missing values:", dataset1_missing)
print("Dataset 2 missing values:", dataset2_missing)


# =====================================================
# 4. STANDARDIZE DISEASE COLUMN
# =====================================================

print("\nStandardizing disease column...")

df1.rename(columns={df1.columns[0]: "disease"}, inplace=True)
df2.rename(columns={df2.columns[0]: "disease"}, inplace=True)


# =====================================================
# 5. REMOVE DUPLICATES
# =====================================================

print("\nRemoving duplicate records...")

before_df1 = len(df1)
before_df2 = len(df2)

df1 = df1.drop_duplicates()
df2 = df2.drop_duplicates()

duplicates_removed_df1 = before_df1 - len(df1)
duplicates_removed_df2 = before_df2 - len(df2)

print("Dataset 1 duplicates removed:", duplicates_removed_df1)
print("Dataset 2 duplicates removed:", duplicates_removed_df2)


# =====================================================
# 6. REMOVE MISSING DISEASE LABELS
# =====================================================

print("\nChecking disease labels...")

missing_disease_df1 = int(df1["disease"].isna().sum())
missing_disease_df2 = int(df2["disease"].isna().sum())

df1 = df1.dropna(subset=["disease"])
df2 = df2.dropna(subset=["disease"])

print(
    "Missing disease labels removed:",
    missing_disease_df1 + missing_disease_df2
)


# =====================================================
# 7. ALIGN SYMPTOM COLUMNS
# =====================================================

print("\nAligning symptom columns...")

symptoms1 = set(df1.columns) - {"disease"}
symptoms2 = set(df2.columns) - {"disease"}

all_symptoms = symptoms1.union(symptoms2)

print("Total symptoms after merge:", len(all_symptoms))

ordered_columns = ["disease"] + sorted(all_symptoms)

df1 = df1.reindex(
    columns=ordered_columns,
    fill_value=0
)

df2 = df2.reindex(
    columns=ordered_columns,
    fill_value=0
)


# =====================================================
# 8. MERGE DATASETS
# =====================================================

print("\nMerging datasets...")

df = pd.concat(
    [df1, df2],
    ignore_index=True
)

print("Merged dataset shape:", df.shape)


# =====================================================
# 9. HANDLE MISSING SYMPTOM VALUES
# =====================================================

print("\nChecking merged dataset for missing values...")

missing_before = int(
    df.isna().sum().sum()
)

symptom_columns_temp = [
    col for col in df.columns
    if col != "disease"
]

# Missing symptom means symptom is absent
df[symptom_columns_temp] = (
    df[symptom_columns_temp]
    .fillna(0)
)

missing_after = int(
    df.isna().sum().sum()
)

print(
    "Missing values before handling:",
    missing_before
)

print(
    "Missing values after handling:",
    missing_after
)


# =====================================================
# 10. REMOVE RARE DISEASES
# =====================================================

print("\nRemoving rare diseases...")

disease_counts_before = (
    df["disease"].value_counts()
)

valid_diseases = (
    disease_counts_before[
        disease_counts_before > 1
    ].index
)

rare_rows_removed = int(
    (~df["disease"].isin(valid_diseases)).sum()
)

rare_classes_removed = int(
    (disease_counts_before <= 1).sum()
)

df = df[
    df["disease"].isin(valid_diseases)
].copy()

print(
    "Rare disease classes removed:",
    rare_classes_removed
)

print(
    "Rare disease records removed:",
    rare_rows_removed
)

print(
    "Dataset after filtering:",
    df.shape
)


# =====================================================
# 11. PREPARE FEATURES
# =====================================================

print("\nPreparing feature matrix...")

y = df["disease"]

X = df.drop(
    "disease",
    axis=1
)

# Convert symptoms to integers
X = X.astype("int8")

symptom_columns = X.columns.tolist()

print(
    "Feature matrix:",
    X.shape
)

print(
    "Number of symptoms/features:",
    len(symptom_columns)
)

print(
    "Number of disease classes:",
    y.nunique()
)


# =====================================================
# 12. ENCODE DISEASE LABELS
# =====================================================

print("\nEncoding disease labels...")

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

number_of_classes = len(
    label_encoder.classes_
)

print(
    "Encoded disease classes:",
    number_of_classes
)

print(
    "Example:",
    label_encoder.classes_[0],
    "->",
    y_encoded[0]
)


# =====================================================
# 13. TRAIN TEST SPLIT — 70/30
# =====================================================

print("\nSplitting dataset 70/30...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.30,
    random_state=42,
    stratify=y_encoded
)

print(
    "Training samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)


# =====================================================
# 14. TRAIN XGBOOST MODEL
# =====================================================

print("\nTraining XGBoost model...")

model = XGBClassifier(
    n_estimators=150,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,

    objective="multi:softprob",

    num_class=number_of_classes,

    eval_metric="mlogloss",

    tree_method="hist",

    n_jobs=-1,

    random_state=42
)

model.fit(
    X_train,
    y_train
)

print(
    "XGBoost training completed"
)


# =====================================================
# 15. EVALUATE MODEL
# =====================================================

print("\nEvaluating model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

report = classification_report(
    y_test,
    y_pred,
    output_dict=True,
    zero_division=0
)


print(
    "\nXGBoost Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# =====================================================
# 16. SAVE MODEL METRICS
# =====================================================

print("\nSaving model metrics...")

metrics = {

    "model": {

        "algorithm": "XGBoost",

        "n_estimators": 150,

        "max_depth": 6,

        "learning_rate": 0.1,

        "subsample": 0.8,

        "colsample_bytree": 0.8,

        "objective": "multi:softprob",

        "random_state": 42
    },


    "dataset": {

        "dataset_1": {

            "rows_original":
                int(before_df1),

            "rows_after_duplicate_removal":
                int(len(df1)),

            "duplicates_removed":
                int(duplicates_removed_df1)
        },


        "dataset_2": {

            "rows_original":
                int(before_df2),

            "rows_after_duplicate_removal":
                int(len(df2)),

            "duplicates_removed":
                int(duplicates_removed_df2)
        },


        "merged_rows_before_filtering":
            int(before_df1 + before_df2),


        "merged_rows_after_cleaning":
            int(len(df)),


        "columns":
            int(len(df.columns)),


        "features":
            int(len(symptom_columns)),


        "disease_classes":
            int(y.nunique()),


        "missing_values_before":
            int(missing_before),


        "missing_values_after":
            int(missing_after),


        "duplicate_rows_removed":
            int(
                duplicates_removed_df1 +
                duplicates_removed_df2
            ),


        "rare_disease_classes_removed":
            int(rare_classes_removed),


        "rare_disease_records_removed":
            int(rare_rows_removed)
    },


    "split": {

        "training_samples":
            int(len(X_train)),

        "testing_samples":
            int(len(X_test)),

        "training_ratio":
            0.70,

        "test_size":
            0.30
    },


    "performance": {

        "accuracy":
            round(float(accuracy), 6),

        "accuracy_percent":
            round(float(accuracy * 100), 2),


        "precision_macro":
            round(
                float(
                    report["macro avg"]["precision"]
                ),
                6
            ),


        "recall_macro":
            round(
                float(
                    report["macro avg"]["recall"]
                ),
                6
            ),


        "f1_macro":
            round(
                float(
                    report["macro avg"]["f1-score"]
                ),
                6
            ),


        "precision_weighted":
            round(
                float(
                    report["weighted avg"]["precision"]
                ),
                6
            ),


        "recall_weighted":
            round(
                float(
                    report["weighted avg"]["recall"]
                ),
                6
            ),


        "f1_weighted":
            round(
                float(
                    report["weighted avg"]["f1-score"]
                ),
                6
            )
    }
}


os.makedirs(
    "ml",
    exist_ok=True
)


with open(
    METRICS_PATH,
    "w"
) as f:

    json.dump(
        metrics,
        f,
        indent=4
    )


print(
    "Metrics saved to:",
    METRICS_PATH
)


# =====================================================
# 17. SAVE MODEL
# =====================================================

print("\nSaving model with compression...")

joblib.dump(
    model,
    MODEL_PATH,
    compress=COMPRESSION_LEVEL
)


joblib.dump(
    symptom_columns,
    FEATURE_PATH,
    compress=COMPRESSION_LEVEL
)


joblib.dump(
    label_encoder,
    LABEL_ENCODER_PATH,
    compress=COMPRESSION_LEVEL
)


print(
    "Model saved to:",
    MODEL_PATH
)

print(
    "Symptom columns saved to:",
    FEATURE_PATH
)

print(
    "Disease label encoder saved to:",
    LABEL_ENCODER_PATH
)


print(
    "\nXGBoost training pipeline completed successfully 🚀"
)