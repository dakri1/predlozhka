import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    username TEXT,
    message_count INTEGER DEFAULT 0,
    reset_date TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT
)
''')

cursor.execute('''
INSERT INTO admin (user_id) VALUES ('1290725432')
''')

conn.commit()
conn.close()
print("Таблица успешно создана.")
