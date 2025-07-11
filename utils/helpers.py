import sqlite3

DB_NAME = "chargesmart.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            extra TEXT  -- car model, like 'Tata Nexon'
        )
    """)

    # Business Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS business (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            extra TEXT  -- station name or company name
        )
    """)

    conn.commit()
    conn.close()
