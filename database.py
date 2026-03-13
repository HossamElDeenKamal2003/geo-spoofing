import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users_table (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        default_country TEXT,
        default_ip TEXT,
        default_isp TEXT,
        default_timezone TEXT,
        default_lat REAL,
        default_lng REAL,
        device_id TEXT,
        collected_ip TEXT,
        collected_isp TEXT,
        collected_timezone TEXT,
        collected_lat REAL,
        collected_lng REAL,
        distance_km REAL,
        tz_match BOOLEAN,
        ip_type TEXT,
        spoofing_score REAL,
        verdict TEXT,
        login_timestamp DATETIME,
        permission_granted BOOLEAN DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, default_country, default_ip, default_isp, default_timezone, default_lat, default_lng, device_id=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO users_table 
        (username, password, default_country, default_ip, default_isp, default_timezone, default_lat, default_lng, device_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, password, default_country, default_ip, default_isp, default_timezone, default_lat, default_lng, device_id))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password FROM users_table WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == password