import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    study_hours REAL,
    attendance REAL,
    previous_marks REAL,
    assignment_score REAL,
    internal_marks REAL,
    performance TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")