# backend/validator.py

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_user_input(form_data):
    """
    Validates and cleans structured dropdown-based form input.
    Returns cleaned dictionary if valid.
    Raises ValidationError if invalid.
    """

    try:
        # Required Fields
        name = form_data.get("name", "").strip()
        age = int(form_data.get("age", 0))
        weight = float(form_data.get("weight", 0))
        severity = int(form_data.get("severity", 0))

        # Multi-select dropdowns (Flask sends list)
        symptoms = form_data.getlist("symptoms")
        allergies = form_data.getlist("allergies")
        conditions = form_data.getlist("existing_conditions")

    except Exception:
        raise ValidationError("Invalid input format.")

    # ---- Basic Validations ----

    if not name:
        raise ValidationError("Name is required.")

    if age < 1 or age > 120:
        raise ValidationError("Age must be between 1 and 120.")

    if weight < 1 or weight > 300:
        raise ValidationError("Weight must be realistic.")

    if severity < 1 or severity > 10:
        raise ValidationError("Severity must be between 1 and 10.")

    if not symptoms:
        raise ValidationError("At least one symptom must be selected.")

    # ---- Normalize Data ----

    cleaned_data = {
        "name": name,
        "age": age,
        "weight": weight,
        "severity": severity,
        "symptoms": [s.lower() for s in symptoms],
        "allergies": [a.lower() for a in allergies],
        "existing_conditions": [c.lower() for c in conditions],
    }

    return cleaned_data