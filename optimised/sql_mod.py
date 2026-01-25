import sqlite3



def check_db():
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        filename TEXT NOT NULL,
        key TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor() 
    cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone() #retrieves the first matching row found If no user matches the credentials, user becomes None
    conn.close()
    return user is not None 

def check_exist(username):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user is not None # true if user exists

def register_user(username, password):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO user (username,password) VALUES (?,?)", (username, password))
    conn.commit()
    conn.close()

def save_file(username, filename, key):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO files (username, filename, key) VALUES (?,?,?)", (username, filename, key))
    conn.commit()
    conn.close()

def get_files(username):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE username = ?", (username,))
    files = cur.fetchall()
    conn.close()
    return files

def get_key(username, filename):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("SELECT key FROM files WHERE username = ? AND filename = ?", (username, filename))
    key = cur.fetchone()
    conn.close()
    return key[0] if key else None