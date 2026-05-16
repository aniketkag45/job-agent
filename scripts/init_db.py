from app.services.database import get_connection

connection  = get_connection()

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    apply_link TEXT UNIQUE,
    source TEXT,
    score INTEGER
)
''')
connection.commit()
connection.close()
print("Jobs table created successfully.")