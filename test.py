import pandas as pd

files = [
    "data/Final_Augmented_dataset_Diseases_and_Symptoms.csv",
    "data/expanded_symptoms.csv"
]

for file in files:
    print("\n" + "=" * 60)
    print(file)
    print("=" * 60)

    df = pd.read_csv(file)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Duplicate rows:", df.duplicated().sum())
    print("Total missing values:", df.isna().sum().sum())
    print("Missing values in first column:", df.iloc[:, 0].isna().sum())
    print("Unique diseases:", df.iloc[:, 0].nunique())

    print("\nFirst 10 column names:")
    print(df.columns[:10].tolist())

    print("\nLast 10 column names:")
    print(df.columns[-10:].tolist())

print("\nDone.")