# wireguard-provisioning-service/database.py
import sqlite3

def db_connection():
    return sqlite3.connect('wireguard.db')

def init_db():
    try:
        conn = db_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tokens (token TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS devices (device_id TEXT, public_key TEXT, internal_ip TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def add_token(token):
    conn = db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tokens VALUES (?)", (token,))
    conn.commit()
    conn.close()

def is_token_valid(token):
    conn = db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT token FROM tokens WHERE token = ?", (token,))
        result = c.fetchone()
        return result is not None
    finally:
        conn.close()

def delete_token(token):
    conn = db_connection()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM tokens WHERE token = ?", (token,))
        conn.commit()
    finally:
        conn.close()

def get_next_internal_ip():
    conn = db_connection()
    c = conn.cursor()
    c.execute("SELECT internal_ip FROM devices ORDER BY internal_ip DESC LIMIT 1")
    last_ip = c.fetchone()
    if last_ip is None:
        next_ip = "10.0.0.2"  # Starting IP
    else:
        next_ip = increment_ip(last_ip[0])
    conn.close()
    return next_ip

def increment_ip(ip):
    parts = list(map(int, ip.split('.')))
    parts[-1] += 1  # Increment the last part of the IP
    return '.'.join(map(str, parts))

def create_device_record(device_id, public_key, internal_ip):
    conn = db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO devices (device_id, public_key, internal_ip) VALUES (?, ?, ?)", 
              (device_id, public_key, internal_ip))
    conn.commit()
    conn.close()