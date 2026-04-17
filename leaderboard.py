import sqlite3

def get_leaderboard():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, time_taken FROM players ORDER BY time_taken ASC LIMIT 5")
    data = cursor.fetchall()

    conn.close()
    return data