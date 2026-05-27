from werkzeug.security import generate_password_hash
import sqlite3

DB_PATH = "data/users.db"

email = "yugmahajan2006@gmail.com"
new_password = "Xoxo#1080"

hashed = generate_password_hash(new_password)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute(
    "UPDATE users SET password=? WHERE email=?",
    (hashed, email)
)

conn.commit()
conn.close()

print("Password reset successful.")