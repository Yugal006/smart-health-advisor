# app.py
from backend.doctor_locator import find_nearby_doctors
from backend.location_helper import fix_city_name
from flask import Flask, render_template, request, session, Response
import joblib
from datetime import datetime
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
# -----------------------------
# BACKEND MODULES
# -----------------------------
from backend.blood_donor_engine import (
    init_db,
    register_donor,
    search_donors,
    get_all_donors,
    delete_donor,
    get_blood_group_stats
)

from backend.validator import validate_user_input, ValidationError
from backend.risk_engine import evaluate_risk
from backend.medicine_engine import suggest_medicines
from backend.appointment_engine import recommend_appointment
from backend.formatter import format_final_response
from backend.symptom_analyzer import analyze_symptoms

# -----------------------------
# FLASK INIT
# -----------------------------
app = Flask(__name__)
app.secret_key = "Yugal"

# -----------------------------
# INIT BLOOD DONOR DB
# -----------------------------
init_db()

# -----------------------------
# LOAD SYMPTOM LIST FOR FRONTEND
# -----------------------------
FEATURE_PATH = "ml/symptom_columns.pkl"
symptom_columns = joblib.load(FEATURE_PATH)
ALL_SYMPTOMS = symptom_columns

# -----------------------------
# HOME & INFO PAGES
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    return render_template("index.html", symptoms=ALL_SYMPTOMS)

@app.route("/profile")
def user_profile():
    return render_template("profile.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about_us():
    return render_template("about.html")

# -----------------------------
# SYMPTOM ANALYSIS
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Validate user input
        user_data = validate_user_input(request.form)

        # Analyze symptoms
        ranked_conditions = analyze_symptoms(user_data)

        if ranked_conditions:
            user_data["predicted_condition"] = ranked_conditions[0]["condition"]

        # Risk assessment
        risk_data = evaluate_risk(user_data)

        # Medicine recommendation
        medicine_data = suggest_medicines(ranked_conditions, user_data, risk_data)

        # Appointment recommendation
        appointment_data = recommend_appointment(ranked_conditions, risk_data, user_data)

        # -----------------------------
        # Doctor Locator
        # -----------------------------
        city = user_data.get("city", "")
        area = user_data.get("area", "")

        # Fix spelling mistakes in city
        city = fix_city_name(city)

        # Build search location
        if area:
            search_location = f"{area}, {city}, Maharashtra"
        else:
            search_location = f"{city}, Maharashtra"
        
        user_data["search_location"] = search_location

        doctor_type = appointment_data.get("doctor_type")

        # Find doctors
        nearby_doctors = find_nearby_doctors(doctor_type, search_location)

        appointment_data["nearby_doctors"] = nearby_doctors

        # -----------------------------
        # Format final response
        # -----------------------------
        final_result = format_final_response(
            user_data,
            ranked_conditions,
            risk_data,
            medicine_data,
            appointment_data
        )

        # Save result in session
        session["final_result"] = final_result

        print("Doctor type:", doctor_type)
        print("City:", city)
        print("Doctors found:", nearby_doctors)
        print("Search location:", search_location)
        return render_template(
            "symptom_result.html",
            result=final_result,
            ranked_conditions=ranked_conditions,
            timestamp=datetime.now().strftime("%B %d, %Y %H:%M")
        )

    except ValidationError as e:
        return render_template("error.html", message=str(e))

    except Exception as e:
        print("Unexpected Error:", e)
        return render_template(
            "error.html",
            message="Unexpected error occurred. Please try again."
        )
# -----------------------------
# PDF EXPORT (ReportLab) – Updated with Nearby Doctors
# -----------------------------
@app.route("/export/pdf")
def export_pdf():
    final_result = session.get('final_result')
    if not final_result:
        return render_template("error.html", message="No result to export")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    # -----------------------------
    # Title
    # -----------------------------
    elements.append(Paragraph("Health Analysis Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # -----------------------------
    # User Info
    # -----------------------------
    user = final_result['user']
    elements.append(Paragraph(f"Name: {user['name']}", styles['Normal']))
    elements.append(Paragraph(f"Age: {user['age']}", styles['Normal']))
    elements.append(Paragraph(f"City: {user['city']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # -----------------------------
    # Most Likely Condition
    # -----------------------------
    elements.append(Paragraph("Most Likely Condition:", styles['Heading2']))
    cond = final_result['analysis']['possible_conditions'][0] if final_result['analysis']['possible_conditions'] else None
    if cond:
        elements.append(Paragraph(f"{cond['condition']} ({cond.get('confidence', 'N/A')}%)", styles['Normal']))
        if cond.get('description'):
            elements.append(Paragraph(f"Description: {cond['description']}", styles['Normal']))
    else:
        elements.append(Paragraph("Not identified", styles['Normal']))
    elements.append(Spacer(1, 12))

    # -----------------------------
    # Risk Assessment
    # -----------------------------
    ra = final_result['risk_assessment']
    elements.append(Paragraph("Risk Assessment:", styles['Heading2']))
    elements.append(Paragraph(f"Level: {ra['risk_level'].title()}", styles['Normal']))
    elements.append(Paragraph(f"Score: {ra['risk_score']}", styles['Normal']))
    if ra.get('flags'):
        elements.append(Paragraph("Flags:", styles['Normal']))
        for flag in ra['flags']:
            elements.append(Paragraph(f"- {flag}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # -----------------------------
    # Appointment Advice
    # -----------------------------
    appt = final_result['appointment']
    elements.append(Paragraph("Next Steps:", styles['Heading2']))
    elements.append(Paragraph(f"{appt.get('urgency', 'N/A')}: {appt.get('doctor_type', 'N/A')}", styles['Normal']))
    elements.append(Paragraph(f"Advice: {appt.get('message', '')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # -----------------------------
    # Nearby Doctors
    # -----------------------------
    nearby_doctors = appt.get('nearby_doctors', [])
    if nearby_doctors:
        elements.append(Paragraph("Nearby Doctors & Clinics:", styles['Heading2']))
        for doc_info in nearby_doctors:
            name = doc_info.get('name', 'N/A')
            doc_type = doc_info.get('type', 'N/A')
            distance = doc_info.get('distance')
            distance_str = f"{distance} km" if distance is not None else "Distance N/A"
            description = doc_info.get('description', '')
            elements.append(Paragraph(f"- {name} ({doc_type}, {distance_str})", styles['Normal']))
            if description:
                elements.append(Paragraph(f"  Description: {description}", styles['Normal']))
        elements.append(Spacer(1, 12))

    # -----------------------------
    # Medications
    # -----------------------------
    meds = final_result['medication']
    if meds.get('recommended'):
        elements.append(Paragraph("Recommended Medications:", styles['Heading2']))
        for med in meds['recommended']:
            elements.append(Paragraph(f"- {med}", styles['Normal']))
        elements.append(Spacer(1, 12))

    if meds.get('self_care'):
        elements.append(Paragraph("Self-Care & Recommendations:", styles['Heading2']))
        for advice in meds['self_care']:
            elements.append(Paragraph(f"- {advice}", styles['Normal']))
        elements.append(Spacer(1, 12))

    if meds.get('warnings'):
        elements.append(Paragraph("Critical Warnings:", styles['Heading2']))
        for warning in meds['warnings']:
            elements.append(Paragraph(f"- {warning}", styles['Normal']))
        elements.append(Spacer(1, 12))

    # -----------------------------
    # Timestamp & Disclaimer
    # -----------------------------
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        final_result.get('disclaimer', ''), 
        styles['Italic']
    ))

    doc.build(elements)
    buffer.seek(0)

    return Response(buffer, mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=health_analysis.pdf'})
# -----------------------------
# ADMIN BLOOD DONOR PANEL
# -----------------------------
@app.route("/admin/donors")
def admin_donors():
    donors = get_all_donors()
    stats = get_blood_group_stats()
    labels = [row[0] for row in stats]
    values = [row[1] for row in stats]
    return render_template("admin_donors.html", donors=donors, labels=labels, values=values)

@app.route("/admin/delete/<int:donor_id>")
def admin_delete_donor(donor_id):
    delete_donor(donor_id)
    return render_template("donor_result.html", message="Donor removed successfully.", success=True)

# -----------------------------
# DONOR REGISTRATION
# -----------------------------
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

    success, message = register_donor(name, age, blood_group, city, phone, last_donation)
    return render_template("donor_result.html", message=message, success=success)

# -----------------------------
# DONOR SEARCH
# -----------------------------
@app.route("/donor/search")
def donor_search_page():
    return render_template("donor_search.html")

@app.route("/donor/search", methods=["POST"])
def donor_search():
    blood_group = request.form.get("blood_group")
    city = request.form.get("city")
    results = search_donors(blood_group, city)
    return render_template("donor_result.html", donors=results, search=True, requested_group=blood_group)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)