import sqlite3

connection  = sqlite3.connect('database/jobs.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS verification_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) 
    )
''')
connection.commit()
connection.close()
print("Verification tokens table created successfully.")