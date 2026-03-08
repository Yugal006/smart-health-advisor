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
            "name": user_data["name"],
            "age": user_data["age"]
        },

        "analysis": {
            "top_condition": top_condition,
            "all_possible_conditions": ranked_conditions
        },

        "risk_assessment": {
            "risk_level": risk_data["risk_level"],
            "risk_score": risk_data["risk_score"],
            "flags": risk_data["flags"]
        },

        "medication": {
            "recommended": medicine_data.get("recommended_medicines", []),
            "warnings": medicine_data.get("warnings", [])
        },

        "appointment": appointment_data,

        "disclaimer": (
            "This system provides AI-based health suggestions "
            "for educational purposes only. It does not replace "
            "professional medical advice. Please consult a "
            "licensed healthcare provider for accurate diagnosis."
        )
    }

    return response