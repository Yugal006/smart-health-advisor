class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_user_input(form_data):

    try:
        name = form_data.get("name", "").strip()
        age = int(form_data.get("age", 0))
        weight = float(form_data.get("weight", 0))
        severity = int(form_data.get("severity", 0))

        city = form_data.get("city", "").strip()
        area = form_data.get("area", "").strip()

        symptoms = form_data.getlist("symptoms")

    except Exception:
        raise ValidationError("Invalid input format.")

    # -------------------------
    # Basic Validations
    # -------------------------

    if not name:
        raise ValidationError("Name is required.")

    if age < 1 or age > 120:
        raise ValidationError("Age must be between 1 and 120.")

    if weight < 1 or weight > 300:
        raise ValidationError("Weight must be realistic.")

    if severity < 1 or severity > 10:
        raise ValidationError("Severity must be between 1 and 10.")

    if not symptoms or len(symptoms) < 3:
        raise ValidationError("At least 3 symptoms must be selected.")

    if not city:
        raise ValidationError("City is required.")

    if not area:
        raise ValidationError("Area / Sector is required.")

    # -------------------------
    # Cleaned Data
    # -------------------------

    cleaned_data = {
        "name": name,
        "age": age,
        "weight": weight,
        "severity": severity,
        "city": city,
        "area": area,
        "symptoms": [s.strip().lower() for s in symptoms]
    }

    return cleaned_data