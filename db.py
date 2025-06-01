import sqlite3

def init_db():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_search(city):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('INSERT INTO searches (city) VALUES (?)', (city,))
    conn.commit()
    conn.close()

def get_last_searches(limit=5):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('SELECT city, timestamp FROM searches ORDER BY timestamp DESC LIMIT ?', (limit,))
    results = c.fetchall()
    conn.close()
    return results
