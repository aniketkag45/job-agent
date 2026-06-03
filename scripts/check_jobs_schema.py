from app.services.database import (
    get_connection
)

connection = get_connection()

cursor = connection.cursor()

cursor.execute(

    "PRAGMA table_info(jobs)"

)

columns = cursor.fetchall()

for column in columns:

    print(dict(column))

connection.close()