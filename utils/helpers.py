
import sqlite3

def init_db():
    conn = sqlite3.connect("charge_smart.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, extra TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS business (id INTEGER PRIMARY KEY, username TEXT, password TEXT, extra TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS stations (id INTEGER PRIMARY KEY, name TEXT, owner TEXT, revenue REAL)")
    cursor.execute("INSERT OR IGNORE INTO stations (id, name, owner, revenue) VALUES (1, 'Chennai Central', 'biz1', 12000), (2, 'Velachery Hub', 'biz1', 8000), (3, 'OMR FastCharge', 'biz2', 18000)")
    conn.commit()
    conn.close()
