import sqlite3
from datetime import datetime, timedelta

DB_NAME = "data/donors.db"


# ----------------------------
# DATABASE INITIALIZATION
# ----------------------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            blood_group TEXT NOT NULL,
            city TEXT NOT NULL,
            phone TEXT NOT NULL,
            last_donation DATE,
            available INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# ELIGIBILITY CHECK
# ----------------------------

def is_eligible(age, last_donation):
    """
    Eligibility Rules:
    - Age between 18 and 60
    - Last donation at least 90 days ago
    """

    if age < 18 or age > 60:
        return False, "Age must be between 18 and 60."

    if last_donation:
        last_date = datetime.strptime(last_donation, "%Y-%m-%d")
        if datetime.now() - last_date < timedelta(days=90):
            return False, "Donation gap must be at least 90 days."

    return True, "Eligible"


# ----------------------------
# REGISTER DONOR
# ----------------------------

def register_donor(name, age, blood_group, city, phone, last_donation):

    # Normalize data
    name = name.strip().title()
    city = city.strip().title()
    blood_group = blood_group.strip().upper()

    eligible, message = is_eligible(age, last_donation)

    if not eligible:
        return False, message

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if donor already exists
    cursor.execute("""
        SELECT id FROM donors
        WHERE name=? AND age=? AND blood_group=? AND city=? AND phone=? AND last_donation=?
    """, (name, age, blood_group, city, phone, last_donation))
    
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False, "Donor already exists."

    if cursor.fetchone():
        conn.close()
        return False, "Donor already registered."  #may not be needed since we are checking for existing donor above

    # Insert new donor
    cursor.execute("""
        INSERT INTO donors (name, age, blood_group, city, phone, last_donation, available)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, age, blood_group, city, phone, last_donation, 1))

    conn.commit()
    conn.close()

    return True, "Donor registered successfully."

def get_compatible_donors(recipient_group):

    compatibility = {
        "A+": ["A+", "A-", "O+", "O-"],
        "A-": ["A-", "O-"],
        "B+": ["B+", "B-", "O+", "O-"],
        "B-": ["B-", "O-"],
        "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        "AB-": ["A-", "B-", "AB-", "O-"],
        "O+": ["O+", "O-"],
        "O-": ["O-"]
    }

    return compatibility.get(recipient_group.upper(), [])

# ----------------------------
# SEARCH DONOR
# ----------------------------

def search_donors(blood_group, city):

    blood_group = blood_group.strip().upper()
    city = city.strip().title()

    compatible_groups = get_compatible_donors(blood_group)

    if not compatible_groups:
        return []

    placeholders = ",".join(["?"] * len(compatible_groups))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = f"""
        SELECT name, age, blood_group, city, phone, last_donation
        FROM donors
        WHERE UPPER(blood_group) IN ({placeholders})
        AND LOWER(city) = LOWER(?)
        AND available = 1
    """

    cursor.execute(query, (*compatible_groups, city))
    results = cursor.fetchall()

    conn.close()
    results.sort(key=lambda x: x[2] != blood_group)
    return results 

def get_all_donors():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, age, blood_group, city, phone, last_donation
        FROM donors
        ORDER BY id DESC
    """)

    donors = cursor.fetchall()
    conn.close()

    return donors

def delete_donor(donor_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM donors WHERE id = ?",
        (donor_id,)
    )

    conn.commit()
    conn.close()

def get_blood_group_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT blood_group, COUNT(*)
        FROM donors
        GROUP BY blood_group
    """)

    data = cursor.fetchall()
    conn.close()

    return data
