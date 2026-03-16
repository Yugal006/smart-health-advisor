# backend/formatter.py

def format_final_response(
    user_data,
    ranked_conditions,
    risk_data,
    medicine_data,
    appointment_data
):
    """
    Combines all engine outputs into a structured response
    for frontend rendering.
    """

    top_condition = (
        ranked_conditions[0]["condition"]
        if ranked_conditions else "Not clearly identified"
    )

    response = {

        "user": {
            "name": user_data.get("name", "User"),
            "age": user_data.get("age", "N/A"),
            "city": user_data.get("city", ""),
            "search_location": user_data.get("search_location", "")
        },

        "analysis": {
            "top_condition": top_condition,
            "possible_conditions": ranked_conditions
        },

        "risk_assessment": {
            "risk_level": risk_data.get("risk_level", "unknown"),
            "risk_score": risk_data.get("risk_score", 0),
            "flags": risk_data.get("flags", [])
        },

        "medication": {
            "recommended": medicine_data.get("recommended_medicines", []),
            "self_care": medicine_data.get("self_care", []),
            "warnings": medicine_data.get("warnings", [])
        },

        "appointment": {
        "doctor_type": appointment_data.get("doctor_type"),
        "urgency": appointment_data.get("urgency"),
        "message": appointment_data.get("message"),
        "nearby_doctors": appointment_data.get("nearby_doctors", [])
        },

        "disclaimer": (
            "This AI system provides health suggestions for educational "
            "purposes only and does not replace professional medical advice."
        )
    }

    return response