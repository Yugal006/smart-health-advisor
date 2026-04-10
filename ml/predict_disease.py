from backend.clinical_rules import CLINICAL_RULES
import pandas as pd
import joblib
import os
import re

# =====================================
# PATHS
# =====================================

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "disease_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "symptom_columns.pkl")
INDEX_1 = os.path.join(BASE_DIR, "disease_symptom_map.pkl")
INDEX_2 = os.path.join(BASE_DIR, "symptom_disease_map.pkl")

# =====================================
# LAZY LOADING (IMPORTANT 🔥)
# =====================================

model = None
symptom_columns = None
disease_symptom_map = None
symptom_disease_map = None

def load_resources():
    global model, symptom_columns, disease_symptom_map, symptom_disease_map

    if model is None:
        model = joblib.load(MODEL_PATH)

    if symptom_columns is None:
        symptom_columns = joblib.load(FEATURE_PATH)

    if disease_symptom_map is None:
        disease_symptom_map = joblib.load(INDEX_1)

    if symptom_disease_map is None:
        symptom_disease_map = joblib.load(INDEX_2)

# # =====================================
# # 2. LOAD DATASET
# # =====================================

# DATASET_1 = os.path.join(BASE_DIR, "../data/Final_Augmented_dataset_Diseases_and_Symptoms.csv")
# DATASET_2 = os.path.join(BASE_DIR, "../data/expanded_symptoms.csv")

# df1 = pd.read_csv(DATASET_1)
# df2 = pd.read_csv(DATASET_2)

# df1.rename(columns={df1.columns[0]: "disease"}, inplace=True)
# df2.rename(columns={df2.columns[0]: "disease"}, inplace=True)

# dataset = pd.concat([df1, df2], ignore_index=True)

# # remove rows with missing disease names
# dataset = dataset.dropna(subset=["disease"])

# =====================================
# FAST INDEX STRUCTURES
# =====================================
# Load precomputed symptom-disease indexes for fast lookup
# Built using build_index.py
INDEX_1 = os.path.join(BASE_DIR, "disease_symptom_map.pkl")
INDEX_2 = os.path.join(BASE_DIR, "symptom_disease_map.pkl")

disease_symptom_map = joblib.load(INDEX_1)
symptom_disease_map = joblib.load(INDEX_2)

# =====================================
# 3. SYMPTOM SYNONYMS
# =====================================

SYMPTOM_SYNONYMS = {
    # Respiratory
    "cough": ["dry_cough", "wet_cough"],
    "sore throat": ["sore_throat"],
    "shortness of breath": ["shortness_of_breath", "difficulty_breathing"],
    "runny nose": ["runny_nose", "nasal_discharge"],
    "congestion": ["nasal_congestion", "blocked_nose"],
    "wheezing": ["wheezing"],
    "chest pain": ["chest_pain", "tight_chest"],

    # Fever / General
    "fever": ["fever_high", "fever_low", "temperature"],
    "fatigue": ["fatigue", "tiredness", "exhaustion"],
    "malaise": ["malaise", "general_weakness"],
    "chills": ["chills", "shivering"],

    # Digestive
    "nausea": ["nausea", "feeling_sick"],
    "vomiting": ["vomiting"],
    "diarrhea": ["diarrhea", "loose_stools"],
    "abdominal pain": ["abdominal_pain", "stomach_pain", "sharp_abdominal_pain"],
    "constipation": ["constipation"],
    "loss of appetite": ["loss_of_appetite", "anorexia"],

    # Neurological
    "headache": ["headache", "migraine_headache", "pounding_headache"],
    "dizziness": ["dizziness", "lightheadedness"],
    "confusion": ["confusion", "disorientation"],

    # Skin
    "rash": ["skin_rash", "red_rash", "itchy_rash"],
    "itching": ["itching", "pruritus"],
    "swelling": ["swelling", "edema"],

    # ENT
    "ear pain": ["ear_pain", "otalgia"],
    "hearing loss": ["hearing_loss", "deafness"],
    "tinnitus": ["tinnitus", "ringing_in_ears"],

    # Eye
    "red eyes": ["red_eyes", "conjunctival_injection"],
    "blurred vision": ["blurred_vision"],
    "eye pain": ["eye_pain"],

    # Urinary / Reproductive
    "painful urination": ["painful_urination", "dysuria"],
    "vaginal discharge": ["vaginal_discharge"],
    "vulvar irritation": ["vulvar_irritation"],
    "pelvic pain": ["pelvic_pain"],

    # Musculoskeletal
    "joint pain": ["joint_pain", "arthralgia"],
    "muscle pain": ["muscle_pain", "myalgia"],
    "back pain": ["back_pain", "lumbar_pain"],
    "fracture": ["fracture", "broken_bone"],

    # Cardiovascular
    "palpitations": ["palpitations", "heart_racing"],
    "high blood pressure": ["high_blood_pressure", "hypertension"],
    "low blood pressure": ["low_blood_pressure", "hypotension"],

    # Psychiatric
    "anxiety": ["anxiety", "nervousness"],
    "depression": ["depression", "sadness", "low_mood"],
    "insomnia": ["insomnia", "sleeplessness"],

    # Misc / Others
    "bleeding": ["bleeding", "hemorrhage"],
    "weight loss": ["weight_loss", "unexplained_weight_loss"],
    "weight gain": ["weight_gain"],
    "swelling feet": ["swelling_feet", "edema_feet"],
    "hair loss": ["hair_loss", "alopecia"],
    "cough with phlegm": ["wet_cough"],
    "dry cough": ["dry_cough"],
    "sneezing": ["sneezing"],
    "chest tightness": ["tight_chest"],
    "loss of smell": ["anosmia"],
    "loss of taste": ["ageusia"],
    "joint swelling": ["joint_swelling"],
    "abnormal bleeding": ["abnormal_bleeding"],
    "fever with chills": ["fever_high", "chills"],
    "red spots": ["red_spots"],
    "itchy eyes": ["itchy_eyes"],
    "eye discharge": ["eye_discharge"],
    "ear discharge": ["ear_discharge"],
    "palmar rash": ["palmar_rash"],
    "cold sweats": ["cold_sweats"]
}

# =====================================
# 4. NORMALIZE SYMPTOM
# =====================================

def normalize_symptom(symptom: str):

    s = symptom.strip().lower()
    s = s.replace(" ", "_")
    s = re.sub(r'[^a-z_]', '', s)

    return s

# =====================================
# 5. MAP SYNONYMS
# =====================================

def map_synonyms(symptoms):

    mapped = []

    for s in symptoms:

        s_norm = normalize_symptom(s)
        key = s_norm.replace("_", " ")

        # always keep the original symptom
        mapped.append(s_norm)

        # add synonyms if they exist
        if key in SYMPTOM_SYNONYMS:
            mapped.extend(SYMPTOM_SYNONYMS[key])

    return list(set(mapped))

DISEASE_PREVALENCE = {

    # VERY COMMON
    "common cold": 1.0,
    "influenza": 1.0,
    "viral fever": 1.0,
    "acute bronchitis": 1.0,
    "allergic rhinitis": 1.0,

    # COMMON
    "laryngitis": 0.8,
    "sinusitis": 0.8,
    "gastritis": 0.8,
    "migraine": 0.8,
    "urinary tract infection": 0.8,

    # UNCOMMON
    "herpangina": 0.5,
    "polymyalgia rheumatica": 0.4,

    # RARE
    "muscular dystrophy": 0.2,
    "multiple sclerosis": 0.2,
    "leukemia": 0.2
}


# =====================================
# 6. SYMPTOM MATCH SCORE (FIXED)
# =====================================

def symptom_match_score(user_symptoms, disease_name):

    user_set = set(normalize_symptom(s) for s in user_symptoms)

    disease_symptoms = disease_symptom_map.get(disease_name.lower(), set())

    if not disease_symptoms:
        return 0

    match = len(user_set & disease_symptoms)

    return (match / len(disease_symptoms)) * 100
    
# =====================================
# 6B. BAYESIAN SYMPTOM SCORE
# =====================================
def bayesian_symptom_score(user_symptoms, disease_name):

    user_set = set(normalize_symptom(s) for s in user_symptoms)

    disease_symptoms = disease_symptom_map.get(disease_name.lower(), set())

    if not disease_symptoms:
        return 0

    match = len(user_set & disease_symptoms)

    score = match / (len(user_set) + len(disease_symptoms) - match)

    return score * 100


# =====================================
# 7. CLINICAL RULE BOOST
# =====================================

def apply_clinical_rules(user_symptoms, predictions):

    symptom_set = set(normalize_symptom(s) for s in user_symptoms)

    for rule_name, rule in CLINICAL_RULES.items():

        if len(symptom_set.intersection(rule["symptoms"])) / len(rule["symptoms"]) >= 0.6:

            print("Rule Triggered:", rule_name)

            for p in predictions:

                if p["disease"] in rule["boost"]:

                    print("Boosting:", p["disease"])

                    p["probability"] = min(p["probability"] + 8, 100)

    predictions = sorted(predictions, key=lambda x: x["probability"], reverse=True)

    return predictions

# =====================================
# 8. RARE DISEASE FILTER
# =====================================

# =====================================
# RARE DISEASE LIST
# =====================================

RARE_DISEASES = [

    # Genetic / Congenital
    "turner syndrome",
    "down syndrome",
    "edward syndrome",
    "tuberous sclerosis",
    "neurofibromatosis",
    "cystic fibrosis",
    "wilson disease",
    "vacterl syndrome",
    "g6pd enzyme deficiency",
    "syringomyelia",

    # Rare Neurological
    "amyotrophic lateral sclerosis (als)",
    "huntington disease",
    "guillain barre syndrome",
    "spinocerebellar ataxia",
    "normal pressure hydrocephalus",
    "chronic inflammatory demyelinating polyneuropathy (cidp)",

    # Rare Hematologic
    "polycythemia vera",
    "aplastic anemia",
    "myelodysplastic syndrome",
    "hemophilia",
    "von willebrand disease",

    # Rare Autoimmune
    "systemic lupus erythematosis (sle)",
    "scleroderma",
    "sjogren syndrome",

    # Rare Metabolic
    "hemochromatosis",
    "amyloidosis",

    # Rare Infections / Parasites
    "cysticercosis",
    "trichinosis",
    "aspergillosis",
    "histoplasmosis",

    # Rare Cancers
    "soft tissue sarcoma",
    "bone cancer",
    "pituitary adenoma",
    "carcinoid syndrome",

    # Rare Heart / Vascular
    "thoracic aortic aneurysm",
    "hypertrophic obstructive cardiomyopathy (hocm)",

    # Rare Disorders
    "pemphigus",
    "pseudotumor cerebri",
    "ganglion cyst",
    "osteochondroma",
    "kaposi sarcoma",
]

def filter_rare_diseases(predictions):

    filtered = []

    for p in predictions:

        if p["disease"].lower() in RARE_DISEASES:

            # print("Checking rare disease:", p["disease"], p["probability"])

            if p["probability"] < 35:

                # print("Filtered rare disease:", p["disease"])

                continue

        filtered.append(p)

    return filtered

# =====================================
# 9. MAIN PREDICTION FUNCTION
# =====================================

def predict_disease(user_symptoms, top_k=5):

    load_resources()  # 🔥 IMPORTANT (loads model only when needed)

    if not user_symptoms:

        return [{"disease": "Not clearly identified", "probability": 0}]

    # Map synonyms
    symptoms_mapped = map_synonyms(user_symptoms)

    # Model input
    X_input = pd.DataFrame(columns=symptom_columns)
    X_input.loc[0] = 0

    for s in symptoms_mapped:

        if s in X_input.columns:
            X_input.at[0, s] = 1

    # ML prediction
    probs = model.predict_proba(X_input)[0]
    classes = model.classes_

    results = []
    
    for cls, p in zip(classes, probs):

        ml_score = p * 100

        match_score = symptom_match_score(symptoms_mapped, cls)
        
        bayes_score = bayesian_symptom_score(symptoms_mapped, cls)

        final_score = (
            0.35 * ml_score +
            0.4 * match_score +
            0.25 * bayes_score
        )

        # print(
        #     cls,
        #     "ML:", round(ml_score,2),
        #     "MATCH:", round(match_score,2),
        #     "BAYES:", round(bayes_score,2),
        #     "FINAL:", round(final_score,2)
        # )

        prevalence = DISEASE_PREVALENCE.get(cls.lower(), 0.7)

        final_score = final_score * prevalence

        results.append({
            "disease": cls,
            "probability": round(final_score, 2)
        })

    # Sort
    results = sorted(results, key=lambda x: x["probability"], reverse=True)

    # Apply rules
    results = apply_clinical_rules(user_symptoms, results)

    # Rare disease filter
    results = filter_rare_diseases(results)
    for r in results:
        if r["probability"] < 5:
            r["probability"] = 0
    print("Original Symptoms:", user_symptoms)
    print("Mapped Symptoms:", symptoms_mapped)
    return results[:top_k] if results else [{"disease": "Not clearly identified", "probability": 0}]