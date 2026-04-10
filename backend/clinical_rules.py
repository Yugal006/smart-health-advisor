# backend/clinical_rules.py

CLINICAL_RULES = {

    # ==========================
    # GASTROINTESTINAL
    # ==========================
    "gastrointestinal": {
        "symptoms": {"nausea","vomiting","diarrhea","abdominal_pain","dehydration"},
        "boost": [
            "acute_gastroenteritis",
            "food_poisoning",
            "gastritis",
            "stomach_flu",
            "dehydration_condition"
        ]
    },

    "acid_reflux": {
        "symptoms": {"chest_pain","acid_reflux","burning_stomach","nausea"},
        "boost": [
            "gastroesophageal_reflux_disease",
            "acid_reflux",
            "gastritis"
        ]
    },

    # ==========================
    # FLU / VIRAL INFECTION
    # ==========================
    "flu_like": {
        "symptoms": {"fever","chills","cough","fatigue","body_ache","headache"},
        "boost": [
            "influenza",
            "viral_fever",
            "common_cold",
            "covid_like_viral_illness"
        ]
    },

    "respiratory_infection": {
        "symptoms": {"cough","shortness_of_breath","chest_pain","fatigue"},
        "boost": [
            "bronchitis",
            "pneumonia",
            "respiratory_infection"
        ]
    },

    # ==========================
    # ALLERGY / ENT
    # ==========================
    "allergy": {
        "symptoms": {"sneezing","runny_nose","itchy_eyes","nasal_congestion"},
        "boost": [
            "allergic_rhinitis",
            "seasonal_allergy"
        ]
    },

    "sinus_infection": {
        "symptoms": {"headache","nasal_congestion","facial_pain","runny_nose"},
        "boost": [
            "sinusitis"
        ]
    },

    "ear_infection": {
        "symptoms": {"ear_pain","ear_discharge","hearing_loss"},
        "boost": [
            "otitis_media",
            "ear_infection"
        ]
    },

    # ==========================
    # CARDIOVASCULAR
    # ==========================
    "cardiac_warning": {
        "symptoms": {"chest_pain","shortness_of_breath","sweating","nausea"},
        "boost": [
            "heart_attack",
            "angina",
            "cardiac_event"
        ]
    },

    "blood_pressure": {
        "symptoms": {"dizziness","headache","blurred_vision"},
        "boost": [
            "hypertension",
            "hypotension"
        ]
    },

    # ==========================
    # NEUROLOGICAL
    # ==========================
    "migraine_pattern": {
        "symptoms": {"headache","nausea","sensitivity_to_light"},
        "boost": [
            "migraine"
        ]
    },

    "stroke_warning": {
        "symptoms": {"confusion","dizziness","blurred_vision","weakness"},
        "boost": [
            "stroke",
            "transient_ischemic_attack"
        ]
    },

    # ==========================
    # URINARY TRACT
    # ==========================
    "urinary_infection": {
        "symptoms": {"painful_urination","frequent_urination","lower_abdominal_pain"},
        "boost": [
            "urinary_tract_infection",
            "cystitis"
        ]
    },

    "kidney_issue": {
        "symptoms": {"back_pain","painful_urination","fever"},
        "boost": [
            "kidney_infection",
            "kidney_stone"
        ]
    },

    # ==========================
    # SKIN CONDITIONS
    # ==========================
    "skin_allergy": {
        "symptoms": {"rash","itching","red_spots"},
        "boost": [
            "skin_allergy",
            "dermatitis",
            "hives"
        ]
    },

    "infection_skin": {
        "symptoms": {"skin_rash","swelling","pain"},
        "boost": [
            "skin_infection",
            "cellulitis"
        ]
    },

    # ==========================
    # MUSCULOSKELETAL
    # ==========================
    "muscle_joint": {
        "symptoms": {"joint_pain","muscle_pain","swelling"},
        "boost": [
            "arthritis",
            "muscle_strain",
            "fibromyalgia"
        ]
    },

    "fracture": {
        "symptoms": {"fracture","swelling","severe_pain"},
        "boost": [
            "bone_fracture"
        ]
    },

    # ==========================
    # MENTAL HEALTH
    # ==========================
    "anxiety_pattern": {
        "symptoms": {"anxiety","palpitations","insomnia"},
        "boost": [
            "anxiety_disorder",
            "panic_attack"
        ]
    },

    "depression_pattern": {
        "symptoms": {"depression","fatigue","loss_of_appetite"},
        "boost": [
            "major_depressive_disorder"
        ]
    }

}