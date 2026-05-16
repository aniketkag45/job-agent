from app.services.database import get_connection

connection = get_connection()
cursor = connection.cursor()
try:
   cursor.execute("""
    ALTER TABLE jobs
    ADD COLUMN is_notified INTEGER DEFAULT 0
    """)
   connection.commit()
   print("Added 'is_notified' column.")
except Exception as e:
    print(f"Schema update skipped: {e}")
finally:
    connection.close()
