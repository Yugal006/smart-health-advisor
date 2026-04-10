import requests
import math

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates (Haversine formula)
    Returns distance in KM
    """

    R = 6371  # Earth radius in km

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)


def get_coordinates(location):
    """
    Convert location text to latitude & longitude using Nominatim
    """

    try:
        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }

        r = requests.get(
            GEOCODE_URL,
            params=params,
            headers={"User-Agent": "health-app"}
        )

        data = r.json()

        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon

    except Exception as e:
        print("Geocode error:", e)

    return None, None


def find_nearby_doctors(doctor_type, location):
    """
    Find nearby hospitals / clinics / doctors using OpenStreetMap
    """

    lat, lon = get_coordinates(location)

    print("Doctor search:", doctor_type)
    print("Location:", location)
    print("Coordinates:", lat, lon)
    
    if lat is None:
        print("Location not found")
        return [{"name": "City Hospital", "lat": None, "lon": None, "distance": None}]

    try:
        radius = 12000 if doctor_type.lower() in ["hospital", "clinic"] else 8000
        query = f"""
        [out:json][timeout:25];
        (
            node(around:{radius},{lat},{lon})["amenity"~"hospital|clinic|doctors|pharmacy"];
            way(around:{radius},{lat},{lon})["amenity"~"hospital|clinic|doctors|pharmacy"];
            relation(around:{radius},{lat},{lon})["amenity"~"hospital|clinic|doctors|pharmacy"];

            node(around:{radius},{lat},{lon})["healthcare"];
            way(around:{radius},{lat},{lon})["healthcare"];
            relation(around:{radius},{lat},{lon})["healthcare"];
        );
        out center;
        """

        response = requests.get(
            OVERPASS_URL,
            params={"data": query},
            timeout=20
        )
        data = response.json()

        places = []

        for el in data.get("elements", []):

            tags = el.get("tags", {})

            name = tags.get("name", "Medical Center")

            # Detect place type
            place_type = "hospital"

            amenity = tags.get("amenity", "")
            healthcare = tags.get("healthcare", "")

            if amenity == "pharmacy":
                place_type = "pharmacy"

            elif amenity == "clinic" or healthcare == "clinic":
                place_type = "clinic"

            elif amenity == "doctors" or healthcare == "doctor":
                place_type = "doctor"


            # For nodes
            lat_val = el.get("lat")

            # For ways / relations
            if lat_val is None:
                lat_val = el.get("center", {}).get("lat")

            lon_val = el.get("lon")

            if lon_val is None:
                lon_val = el.get("center", {}).get("lon")


            if lat_val and lon_val:

                distance = calculate_distance(lat, lon, lat_val, lon_val)

                places.append({
                    "name": name,
                    "lat": lat_val,
                    "lon": lon_val,
                    "distance": distance,
                    "type": place_type
                })


        # Sort by nearest hospital
        places.sort(key=lambda x: x["distance"])
        print("Places found:", len(places))
        print("Nearest hospital:", places[0] if places else "None")

        if places:
            return places[:15]

    except Exception as e:
        print("Overpass error:", e)

    # fallback
    return [{
        "name": "City Government Hospital",
        "lat": None,
        "lon": None,
        "distance": None,
        "type": doctor_type
    }]