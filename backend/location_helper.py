# backend/location_helper.py
import difflib
import json

# Load from JSON file
with open("data/maharashtra_cities.json") as f:
    KNOWN_CITIES = json.load(f)  # list of city names

def fix_city_name(user_input):
    user_input = user_input.strip().lower()

    # Try exact match first
    for city in KNOWN_CITIES:
        if city.lower() == user_input:
            return city

    # Fuzzy match
    matches = difflib.get_close_matches(user_input, KNOWN_CITIES, n=1, cutoff=0.6)
    if matches:
        return matches[0]

    # fallback: return as-is
    return user_input