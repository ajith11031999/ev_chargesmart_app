import sqlite3

def init_db():
    conn = sqlite3.connect("chargesmart.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, extra TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS business (id INTEGER PRIMARY KEY, username TEXT, password TEXT, extra TEXT)")
    conn.commit()
    conn.close()
