import sqlite3

conn = sqlite3.connect("burnoutguard.db")
rows = conn.execute("SELECT * FROM checkins").fetchall()

for row in rows:
    print(row)

conn.close()
