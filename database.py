import sqlite3

conn = sqlite3.connect("hos.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    heart_risk TEXT,
    diabetes_risk TEXT,
    health_score INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully!")