from flask import Flask, render_template, request

# Blood Donor System
from backend.blood_donor_engine import (
    init_db,
    register_donor,
    search_donors,
    get_all_donors,
    delete_donor,
    get_blood_group_stats
)

# AI Medical Backend
from backend.validator import validate_user_input, ValidationError
from backend.symptom_analyzer import analyze_symptoms
from backend.risk_engine import evaluate_risk
from backend.medicine_engine import suggest_medicines
from backend.appointment_engine import recommend_appointment
from backend.formatter import format_final_response

import pandas as pd

app = Flask(__name__)

def load_symptoms():
    file1 = pd.read_csv("data/expanded_symptoms.csv")
    file2 = pd.read_csv("data/Final_Augmented_dataset_Diseases_and_Symptoms.csv")

    symptoms1 = list(file1.columns[1:])
    symptoms2 = list(file2.columns[1:])

    all_symptoms = sorted(list(set(symptoms1 + symptoms2)))

    return all_symptoms

ALL_SYMPTOMS = load_symptoms()

# Initialize donor database

init_db()

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", symptoms=ALL_SYMPTOMS)


# ---------------------------------------------------
# SYMPTOM ANALYSIS
# ---------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        # 1️⃣ Validate Input
        user_data = validate_user_input(request.form)

        # 2️⃣ ML Disease Prediction
        ranked_conditions = analyze_symptoms(user_data)

        # 3️⃣ Risk Evaluation
        risk_data = evaluate_risk(user_data)

        # 4️⃣ Medicine Suggestions
        medicine_data = suggest_medicines(
            ranked_conditions,
            user_data,
            risk_data
        )

        # 5️⃣ Doctor Recommendation
        appointment_data = recommend_appointment(ranked_conditions, risk_data, user_data)

        # 6️⃣ Combine Everything
        final_result = format_final_response(
            user_data,
            ranked_conditions,
            risk_data,
            medicine_data,
            appointment_data
        )

        return render_template(
            "symptom_result.html",
            result=final_result,
            ranked_conditions=ranked_conditions
        )

    except ValidationError as e:

        return render_template(
            "error.html",
            message=str(e)
        )

    except Exception as e:

        print("Unexpected Error:", e)

        return render_template(
            "error.html",
            message="Unexpected error occurred. Please try again."
        )


# ---------------------------------------------------
# ADMIN DONOR PANEL
# ---------------------------------------------------

@app.route("/admin/donors")
def admin_donors():

    donors = get_all_donors()
    stats = get_blood_group_stats()

    labels = [row[0] for row in stats]
    values = [row[1] for row in stats]

    return render_template(
        "admin_donors.html",
        donors=donors,
        labels=labels,
        values=values
    )


@app.route("/admin/delete/<int:donor_id>")
def admin_delete_donor(donor_id):

    delete_donor(donor_id)

    return render_template(
        "donor_result.html",
        message="Donor removed successfully.",
        success=True
    )


# ---------------------------------------------------
# DONOR REGISTRATION
# ---------------------------------------------------

@app.route("/donor/register")
def donor_register_page():
    return render_template("donor_register.html")


@app.route("/donor/register", methods=["POST"])
def donor_register():

    name = request.form.get("name")
    age = int(request.form.get("age"))
    blood_group = request.form.get("blood_group")
    city = request.form.get("city")
    phone = request.form.get("phone")
    last_donation = request.form.get("last_donation")

    success, message = register_donor(
        name,
        age,
        blood_group,
        city,
        phone,
        last_donation
    )

    return render_template(
        "donor_result.html",
        message=message,
        success=success
    )


# ---------------------------------------------------
# DONOR SEARCH
# ---------------------------------------------------

@app.route("/donor/search")
def donor_search_page():
    return render_template("donor_search.html")


@app.route("/donor/search", methods=["POST"])
def donor_search():

    blood_group = request.form.get("blood_group")
    city = request.form.get("city")

    results = search_donors(blood_group, city)

    return render_template(
        "donor_result.html",
        donors=results,
        search=True,
        requested_group=blood_group
    )


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)