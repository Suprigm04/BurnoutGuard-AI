import sqlite3

conn = sqlite3.connect("burnoutguard.db")
conn.execute("ALTER TABLE checkins ADD COLUMN username TEXT DEFAULT 'testuser'")
conn.commit()
conn.close()
print("Done!")
