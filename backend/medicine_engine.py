# backend/medicine_engine.py
import os
import csv

# ---------------------------------------------------
# File Paths
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDICATIONS_CSV_PATH = os.path.join(BASE_DIR, "data", "medical_dataset.csv")

# ---------------------------------------------------
# Load Condition → Medicines Mapping
# ---------------------------------------------------
def load_condition_medicine_map():
    condition_map = {}
    try:
        with open(MEDICATIONS_CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                disease = row["Disease"].strip().lower()
                medication = row.get("Medication", "").strip()
                recommendation = row.get("Recommendation", "Doctor Required").strip()

                if medication:
                    medicines = [m.strip() for m in medication.split(";") if m.strip()]
                else:
                    medicines = []

                condition_map[disease] = {
                    "medicines": medicines,
                    "recommendation": recommendation
                }
    except Exception as e:
        print("Error loading medication dataset:", e)

    return condition_map

CONDITION_MEDICINE_MAP = load_condition_medicine_map()


# ---------------------------------------------------
# Self-Care Advice (50+ Conditions)
# ---------------------------------------------------
SELF_CARE_ADVICE = {
    "cystitis": [
        "Drink plenty of water to flush bacteria",
        "Avoid caffeine, alcohol, and sugary drinks",
        "Maintain hygiene after using the toilet",
        "Urinate regularly and completely",
        "Consult a doctor if symptoms worsen or persist"
    ],
    "gastritis": [
        "Avoid spicy, oily, and acidic foods",
        "Eat smaller, frequent meals",
        "Avoid alcohol and smoking",
        "Manage stress",
        "Take antacids if recommended"
    ],
    "laryngitis": [
        "Rest your voice",
        "Drink warm fluids",
        "Use a humidifier",
        "Avoid smoking and irritants",
        "Gargle with warm salt water"
    ],
    "common cold": [
        "Rest well",
        "Drink warm fluids",
        "Use steam inhalation or saline spray",
        "Wash hands regularly",
        "Consider vitamin C or zinc"
    ],
    "flu": [
        "Rest and hydrate",
        "Take paracetamol or ibuprofen for fever",
        "Avoid close contact",
        "Eat light, nutritious meals",
        "Monitor for complications"
    ],
    "migraine": [
        "Rest in a dark, quiet room",
        "Stay hydrated",
        "Use cold/warm compresses",
        "Avoid trigger foods",
        "Track triggers for prevention"
    ],
    "insomnia": [
        "Maintain a sleep schedule",
        "Avoid caffeine/heavy meals before bed",
        "Create a calm sleeping environment",
        "Limit screen time",
        "Practice relaxation techniques"
    ],
    "anxiety": [
        "Practice deep breathing or meditation",
        "Exercise regularly",
        "Limit caffeine and alcohol",
        "Talk to friends or family",
        "Try mindfulness or journaling"
    ],
    "dehydration": [
        "Drink water regularly",
        "Include electrolyte drinks if needed",
        "Avoid alcohol and excess caffeine",
        "Eat water-rich fruits and vegetables",
        "Rest in a cool place"
    ],
    "sprain": [
        "Rest the injured area",
        "Apply ice 15-20 min every 2-3 hours",
        "Compress with an elastic bandage",
        "Elevate the limb",
        "Avoid activities that worsen pain"
    ],
    "back pain": [
        "Maintain good posture",
        "Avoid heavy lifting",
        "Apply heat or cold packs",
        "Gentle stretching and movement",
        "Consult a doctor if severe"
    ],
    "eczema": [
        "Keep skin moisturized",
        "Avoid irritants and harsh soaps",
        "Take lukewarm showers",
        "Wear loose, breathable clothing",
        "Use prescribed topical creams"
    ],
    "psoriasis": [
        "Moisturize regularly",
        "Avoid scratching",
        "Use gentle skin products",
        "Manage stress",
        "Follow prescribed treatments"
    ],
    "constipation": [
        "Increase fiber intake",
        "Drink plenty of water",
        "Exercise regularly",
        "Avoid delaying bathroom visits",
        "Consider mild laxatives if recommended"
    ],
    "diarrhea": [
        "Stay hydrated",
        "Eat bland foods (BRAT diet)",
        "Avoid fatty/spicy foods",
        "Rest and monitor symptoms",
        "Seek medical attention if severe"
    ],
    "heartburn/acid reflux": [
        "Avoid spicy, fatty, and acidic foods",
        "Eat smaller meals",
        "Avoid lying down after meals",
        "Maintain healthy weight",
        "Consider antacids if needed"
    ],
    "hypertension": [
        "Reduce salt intake",
        "Exercise regularly",
        "Maintain a healthy weight",
        "Limit alcohol and avoid smoking",
        "Monitor blood pressure"
    ],
    "hypotension": [
        "Drink plenty of water",
        "Eat small, frequent meals",
        "Stand up slowly",
        "Increase salt intake if advised",
        "Wear compression stockings if recommended"
    ],
    "diabetes": [
        "Monitor blood sugar regularly",
        "Maintain a healthy diet",
        "Exercise consistently",
        "Avoid excessive sugar",
        "Follow medication plan"
    ],
    "obesity": [
        "Follow a balanced diet",
        "Exercise regularly",
        "Monitor calorie intake",
        "Avoid sugary and processed foods",
        "Seek professional guidance"
    ],
    "allergies": [
        "Avoid allergens",
        "Take antihistamines if needed",
        "Keep windows closed during high pollen",
        "Shower after being outdoors",
        "Use air purifiers at home"
    ],
    "asthma": [
        "Avoid triggers like smoke and dust",
        "Use inhalers as prescribed",
        "Stay active with gentle exercise",
        "Monitor breathing",
        "Seek immediate help if attack is severe"
    ],
    "bronchitis": [
        "Rest and stay hydrated",
        "Use a humidifier",
        "Avoid smoking and irritants",
        "Take prescribed medications",
        "Consult a doctor if symptoms worsen"
    ],
    "pneumonia": [
        "Rest and drink fluids",
        "Take prescribed antibiotics",
        "Monitor breathing and fever",
        "Avoid exertion",
        "Seek immediate medical care if severe"
    ],
    "sinusitis": [
        "Use saline nasal spray",
        "Apply warm compress on face",
        "Stay hydrated",
        "Rest",
        "Consult doctor if symptoms persist"
    ],
    "tonsillitis": [
        "Rest and hydrate",
        "Gargle warm salt water",
        "Eat soft, soothing foods",
        "Take pain relievers if needed",
        "Consult doctor if severe or recurring"
    ],
    "ear infection": [
        "Avoid inserting objects into ear",
        "Keep ear dry",
        "Take prescribed medications",
        "Pain relief with paracetamol",
        "Seek medical care if fever or discharge"
    ],
    "eye strain": [
        "Follow 20-20-20 rule",
        "Adjust screen brightness",
        "Blink regularly",
        "Use artificial tears if needed",
        "Take frequent breaks from screens"
    ],
    "dry eyes": [
        "Use lubricating eye drops",
        "Take screen breaks",
        "Humidify rooms",
        "Stay hydrated",
        "Protect eyes from wind/dust"
    ],
    "acne": [
        "Clean face gently twice daily",
        "Avoid picking or squeezing pimples",
        "Use non-comedogenic skincare products",
        "Maintain a healthy diet",
        "Follow dermatologist advice if needed"
    ],
    "cold sores": [
        "Avoid touching sores",
        "Use antiviral creams if prescribed",
        "Stay hydrated",
        "Manage stress",
        "Avoid close contact with others during outbreaks"
    ],
    "chickenpox": [
        "Rest and stay hydrated",
        "Avoid scratching blisters",
        "Use calamine lotion for itching",
        "Maintain hygiene",
        "Consult doctor if severe or high fever"
    ],
    "measles": [
        "Rest and hydrate",
        "Use fever-reducing medications",
        "Isolate to prevent spreading",
        "Keep skin clean",
        "Seek medical care immediately"
    ],
    "mumps": [
        "Rest and hydrate",
        "Apply warm/cold compress for swelling",
        "Eat soft foods if jaw pain",
        "Isolate to prevent spreading",
        "Consult doctor if complications arise"
    ],
    "whooping cough": [
        "Rest and hydrate",
        "Use humidified air to ease coughing",
        "Follow prescribed antibiotics",
        "Isolate to prevent spreading",
        "Seek medical care if severe"
    ],
    "tuberculosis": [
        "Follow full course of prescribed antibiotics",
        "Eat a nutritious diet",
        "Rest and avoid stress",
        "Avoid close contact during contagious period",
        "Monitor symptoms and report any worsening"
    ],
    "hepatitis A/B/C": [
        "Follow medical treatment plans",
        "Rest and hydrate",
        "Avoid alcohol",
        "Eat a balanced, nutritious diet",
        "Practice safe hygiene and avoid sharing personal items"
    ],
    "urinary tract infection (UTI)": [
        "Drink plenty of water",
        "Urinate frequently",
        "Maintain hygiene",
        "Avoid irritants like caffeine and alcohol",
        "Seek medical attention if symptoms persist"
    ],
    "kidney stones": [
        "Drink plenty of water",
        "Avoid excessive salt and oxalate-rich foods",
        "Pain relief as prescribed",
        "Rest and monitor symptoms",
        "Seek immediate help if severe pain occurs"
    ],
    "gout": [
        "Avoid purine-rich foods (red meat, seafood)",
        "Stay hydrated",
        "Take prescribed medications",
        "Rest affected joint",
        "Monitor for flare-ups"
    ],
    "arthritis": [
        "Gentle exercise to maintain mobility",
        "Apply heat/cold to affected joints",
        "Maintain healthy weight",
        "Use supportive devices if needed",
        "Follow prescribed treatments"
    ],
    "osteoporosis": [
        "Consume calcium and vitamin D",
        "Engage in weight-bearing exercises",
        "Avoid smoking and excessive alcohol",
        "Prevent falls at home",
        "Follow doctor’s advice for medications"
    ],
    "anemia": [
        "Eat iron-rich foods (meat, leafy greens)",
        "Include vitamin C for better absorption",
        "Avoid excessive tea/coffee with meals",
        "Take supplements if prescribed",
        "Rest when feeling fatigued"
    ],
    "vitamin deficiency": [
        "Eat a balanced diet",
        "Include fruits and vegetables",
        "Take supplements if needed",
        "Get sunlight for vitamin D",
        "Consult a doctor for severe deficiencies"
    ],
    "hypothyroidism": [
        "Take medications as prescribed",
        "Eat a balanced diet",
        "Exercise moderately",
        "Monitor symptoms regularly",
        "Avoid excess soy and raw cruciferous vegetables if advised"
    ],
    "hyperthyroidism": [
        "Take medications as prescribed",
        "Avoid stimulants like caffeine",
        "Maintain adequate rest",
        "Eat a balanced diet",
        "Monitor heart rate and symptoms"
    ],
    "depression": [
        "Talk to someone you trust",
        "Engage in regular physical activity",
        "Maintain a healthy routine",
        "Avoid alcohol and drugs",
        "Seek professional help"
    ],
    "default": [
        "Rest",
        "Drink fluids",
        "Monitor symptoms",
        "Maintain hygiene and nutrition",
        "Consult a doctor if condition worsens or persists"
    ]
}

# ---------------------------------------------------
# Medicine Suggestion Engine
# ---------------------------------------------------
# ---------------------------------------------------
# Suggest Medicines Engine (Top 3 Conditions + UX Friendly)
# ---------------------------------------------------
def suggest_medicines(ranked_conditions, user_data=None, risk_data=None, top_n=3):
    """
    Returns recommended medicines, combined self-care advice, and warnings
    for top N predicted conditions.
    """

    user_data = user_data or {}
    risk_data = risk_data or {}
    age = user_data.get("age", 0)
    risk_level = risk_data.get("risk_level", "low")

    recommended_medicines = set()
    combined_self_care = set()
    warnings = []

    if not ranked_conditions:
        return {
            "recommended_medicines": [],
            "self_care": SELF_CARE_ADVICE["default"],
            "warnings": ["No condition identified. Monitor symptoms and consult doctor if needed."]
        }

    # Process top N conditions
    for cond in ranked_conditions[:top_n]:
        condition_name = cond["condition"].lower().strip()
        condition_data = CONDITION_MEDICINE_MAP.get(condition_name)

        # Get self-care for this condition
        self_care_list = SELF_CARE_ADVICE.get(condition_name, SELF_CARE_ADVICE["default"])
        combined_self_care.update(self_care_list)

        if condition_data:
            recommendation = condition_data["recommendation"].lower()

            if recommendation == "doctor required":
                warnings.append(f"{condition_name.title()} requires medical consultation.")
                continue

            elif recommendation == "emergency":
                warnings.append(f"{condition_name.title()} is an emergency — seek immediate medical attention!")
                continue

            else:
                # Add medicines, checking age restrictions if any
                for med in condition_data["medicines"]:
                    med_clean = med.strip().title()
                    if age < 12 and med_clean.lower() in ["ibuprofen"]:
                        warnings.append(f"{med_clean} is not recommended for children under 12.")
                        continue
                    recommended_medicines.add(med_clean)

        else:
            warnings.append(f"No medication data available for {condition_name.title()}.")

    # High-risk override
    if risk_level in ["high", "emergency"]:
        warnings.append("High risk detected — consult a doctor immediately.")
        recommended_medicines = set()  # Remove OTC meds for safety

    return {
        "recommended_medicines": sorted(list(recommended_medicines)),
        "self_care": sorted(list(combined_self_care)),
        "warnings": warnings
    }