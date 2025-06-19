import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(id)
)
""")

cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (?, ?)", (1, "Smartfonlar"))
cursor.execute("""
INSERT INTO products (name, description, price, category_id)
VALUES (?, ?, ?, ?)
""", ("iPhone 13", "Apple smartfoni", 12990000, 1))

conn.commit()
conn.close()

print("✅ shop.db yaratildi va boshlang‘ich ma'lumotlar qo‘shildi.")
