import sqlite3
import time

def save_player(name, time_taken):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        time_taken REAL
    )
    """)

    cursor.execute("INSERT INTO players (name, time_taken) VALUES (?, ?)",
                   (name, time_taken))

    conn.commit()
    conn.close()