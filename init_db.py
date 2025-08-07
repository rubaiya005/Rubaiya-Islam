import sqlite3

conn = sqlite3.connect('database.db')

# Create 'user' table
conn.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create 'banned_user' table
conn.execute('''
    CREATE TABLE IF NOT EXISTS banned_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("✅ Database and tables created.")
