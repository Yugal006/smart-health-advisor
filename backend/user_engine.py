# backend/user_engine.py

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "data/users.db"


# -----------------------------
# INIT DATABASE
# -----------------------------
def init_user_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


# -----------------------------
# REGISTER USER
# -----------------------------
def register_user(email, password, name=None, is_admin=0):
    hashed = generate_password_hash(password)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (email, password, name, is_admin) VALUES (?, ?, ?, ?)",
            (email, hashed, name, is_admin)
        )
        conn.commit()
        return True, "User registered successfully."

    except sqlite3.IntegrityError:
        return False, "Email already exists."

    finally:
        conn.close()


# -----------------------------
# AUTHENTICATE USER
# -----------------------------
def authenticate_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, password, name, is_admin FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        return {
            "id": user[0],
            "email": email,
            "name": user[2],
            "is_admin": user[3]
        }
    return None


# -----------------------------
# MAKE ADMIN (UTILITY FUNCTION)
# -----------------------------
def make_admin(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET is_admin = 1 WHERE email=?", (email,))
    conn.commit()
    conn.close()


def update_user_details(user_id, name, email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute(
            "UPDATE users SET name=?, email=? WHERE id=?",
            (name, email, user_id)
        )
        conn.commit()
        return True, "Profile updated successfully"
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    finally:
        conn.close()

def update_password(user_id, old_password, new_password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE id=?", (user_id,))
    user = c.fetchone()

    if not user or not check_password_hash(user[0], old_password):
        conn.close()
        return False, "Incorrect current password"

    new_hashed = generate_password_hash(new_password)

    c.execute("UPDATE users SET password=? WHERE id=?", (new_hashed, user_id))
    conn.commit()
    conn.close()

    return True, "Password updated successfully"

def get_all_users():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, is_admin FROM users")
    users = cursor.fetchall()

    conn.close()
    return users


def delete_user_by_admin(user_id):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()