# Smart Health Advisor (CodeCure)

### AI-Powered Smart Health Advisor using Flask & Machine Learning

Smart Health Advisor (CodeCure) is a healthcare assistance platform that combines Machine Learning, Flask, and location-based services to provide preliminary health insights based on user symptoms. The system analyzes symptoms, estimates disease probabilities, assesses risk levels, recommends self-care measures, and helps users locate nearby healthcare facilities.

In addition, the platform includes a Blood Donor Management System that allows users to register as donors and search for compatible blood donors within their city.

> **Disclaimer:** This project is developed for educational and research purposes only and does not replace professional medical advice, diagnosis, or treatment.

---

## Live Demo

**Deployed Application:**
https://smart-health-advisor-qil4.onrender.com/

---

## Features

### AI-Based Symptom Analysis

* Symptom-based disease prediction
* Probability-based diagnosis ranking
* Differential diagnosis generation
* Symptom severity assessment
* Risk level evaluation

### Personalized Health Recommendations

* Self-care suggestions
* Medication recommendations
* Critical warning alerts
* Doctor consultation guidance

### Location-Based Healthcare Support

* Nearby hospital and clinic locator
* Area-specific healthcare recommendations
* Interactive map integration

### Blood Donor Management System

* Donor registration portal
* Blood donor search by city
* Blood group compatibility matching
* Donor database management

### User Management

* User registration and login
* Profile management
* Health report generation
* PDF export functionality

### Administrative Features

* User management dashboard
* Blood donor management
* Database monitoring

---

## Machine Learning Pipeline

The disease prediction engine is trained using healthcare datasets collected from Kaggle and augmented symptom datasets.

### Workflow

1. Load healthcare datasets
2. Align symptom columns across datasets
3. Merge datasets
4. Remove rare disease classes
5. Create symptom feature vectors
6. Train Machine Learning model
7. Evaluate performance
8. Save trained model for deployment

### Model Used

**Random Forest Classifier**

Configuration:

```python
RandomForestClassifier(
    n_estimators=120,
    max_depth=25,
    min_samples_split=5,
    random_state=42
)
```

### Prediction Process

User Inputs:

* Age
* Weight
* Gender
* Location
* Symptoms
* Symptom Severity

System Outputs:

* Most probable condition
* Disease probability ranking
* Risk assessment score
* Self-care recommendations
* Medication suggestions
* Healthcare guidance

---

## 📸 Project Screenshots

### Application Overview

<p align="center">
  <img src="static/images/screenshots/Home.png" width="45%" alt="Home Page">
  <img src="static/images/screenshots/Symptom_input.png" width="45%" alt="Symptom Input">
</p>

<p align="center">
  <em>Home Page</em> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <em>Symptom Analysis Form</em>
</p>

---

### AI Analysis Reports

<p align="center">
  <img src="static/images/screenshots/Report_1.png" width="45%" alt="Report 1">
  <img src="static/images/screenshots/Report_2.png" width="45%" alt="Report 2">
</p>

<p align="center">
  <em>Disease Prediction Report</em> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <em>Recommendations & Hospital Locator</em>
</p>

---

### Blood Donor Management System

<p align="center">
  <img src="static/images/screenshots/Donor_reg.png" width="45%" alt="Donor Search">
  <img src="static/images/screenshots/Donor_Result.png" width="45%" alt="Donor Results">
</p>

<p align="center">
  <em>Donor Registration</em> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <em>Matching Donor Results</em>
</p>

---

### User & Administration

<p align="center">
  <img src="static/images/screenshots/Profile.png" width="45%" alt="Profile">
  <img src="static/images/screenshots/admin_panel.png" width="45%" alt="Admin Panel">
</p>

<p align="center">
  <em>User Profile</em> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <em>Admin Dashboard</em>
</p>

---

### System Architecture

<p align="center">
  <img src="static/images/screenshots/flowchart.png" width="45%" alt="Flowchart">
  <img src="static/images/screenshots/ml_pipeline.png" width="45%" alt="ML Pipeline">
</p>

<p align="center">
  <em>System Flowchart</em> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <em>Machine Learning Pipeline</em>
</p>


## Tech Stack

### Backend

* Python
* Flask
* SQLite

### Machine Learning

* Scikit-Learn
* Pandas
* Joblib

### Frontend

* HTML5
* CSS3
* JavaScript

### Maps & Location Services

* OpenStreetMap
* Leaflet.js

### Deployment

* Render

---

### Backend Modules

| Module                | Purpose                   |
| --------------------- | ------------------------- |
| symptom_analyzer.py   | Symptom processing        |
| risk_engine.py        | Risk evaluation           |
| medicine_engine.py    | Recommendation generation |
| clinical_rules.py     | Healthcare rules engine   |
| doctor_locator.py     | Hospital discovery        |
| blood_donor_engine.py | Donor matching            |
| user_engine.py        | User management           |
| validator.py          | Input validation          |

---

## Datasets

The project uses healthcare datasets containing diseases and symptom mappings.

Primary datasets include:

* Final_Augmented_dataset_Diseases_and_Symptoms.csv
* expanded_symptoms.csv
* Symptom-severity.csv

These datasets were preprocessed and merged to create a unified symptom prediction model.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Yugal006/smart-health-advisor.git
cd smart-health-advisor
```

### Create Virtual Environment

```bash
python -m venv venv
```

Linux/Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Future Enhancements

* Improved dataset coverage
* Enhanced prediction accuracy
* Integration with healthcare APIs
* Appointment booking support
* Medical report uploads
* AI chatbot assistance
* Mobile application version

---
