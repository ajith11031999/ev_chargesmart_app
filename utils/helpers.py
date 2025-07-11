
import sqlite3

def init_db():
    conn = sqlite3.connect("chargesmart.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, extra TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS business (id INTEGER PRIMARY KEY, username TEXT, password TEXT, extra TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, user TEXT, station TEXT, slot TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS stations (id INTEGER PRIMARY KEY, name TEXT, location TEXT, plug_type TEXT, slots INTEGER, available INTEGER, wait_time INTEGER, owner TEXT, avg_time INTEGER, revenue REAL)")
    conn.commit()
    conn.close()
