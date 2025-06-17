import sqlite3
import random

def get_random_questions(limit=5):
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    rows = c.fetchall()
    conn.close()
    return random.sample(rows, min(limit, len(rows)))
