import sqlite3

# Baza yaratish
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

# Savollar jadvali
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    correct TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL
)
""")

# Savollarni qo‘shish
cursor.executemany("""
INSERT INTO questions (country, correct, option1, option2, option3)
VALUES (?, ?, ?, ?, ?)
""", [
    ('France', 'Paris', 'Lyon', 'Marseille', 'Nice'),
    ('Germany', 'Berlin', 'Munich', 'Frankfurt', 'Hamburg'),
    ('Italy', 'Rome', 'Milan', 'Naples', 'Turin'),
    ('Uzbekistan', 'Tashkent', 'Samarkand', 'Bukhara', 'Andijan'),
])

conn.commit()
conn.close()

