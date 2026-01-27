import sqlite3

def est_conn(func):
    def Wrapper(*args, **kwargs):
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        # Execute the function once and store its return value
        result = func(cur, *args, **kwargs)
        conn.commit()
        conn.close()
        # Return the stored value
        return result
    return Wrapper


@est_conn
def check_db(cur):
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

@est_conn
def check_login(cur, username, password):
    cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone() #retrieves the first matching row found If no user matches the credentials, user becomes None
    return user is not None 

@est_conn
def check_exist(cur, username):
    cur.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cur.fetchone()
    return user is not None # true if user exists

@est_conn
def register_user(cur, username, password):
    cur.execute("INSERT INTO user (username,password) VALUES (?,?)", (username, password))

@est_conn
def save_file(cur, username, filename, key):
    cur.execute("INSERT INTO files (username, filename, key) VALUES (?,?,?)", (username, filename, key))

@est_conn
def get_files(cur, username):
    cur.execute("SELECT * FROM files WHERE username = ?", (username,))
    files = cur.fetchall()
    return files

@est_conn
def get_key(cur, username, filename):
    cur.execute("SELECT key FROM files WHERE username = ? AND filename = ?", (username, filename))
    key = cur.fetchone()
    return key[0] if key else None #ftch1 returns a string in a tuple