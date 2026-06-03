import sqlite3
import bcrypt


def init_users_db():
    conn = sqlite3.connect("burnoutguard.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.commit()
    conn.close()


def create_user(username, password, role="user"):
    conn = sqlite3.connect("burnoutguard.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, hashed, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username, password):
    conn = sqlite3.connect("burnoutguard.db")
    c = conn.cursor()
    c.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode(), result[0]):
        return result[1]
    return None
