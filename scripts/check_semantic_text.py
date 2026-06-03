from app.services.database import (
    get_connection
)

connection = get_connection()

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        title,
        semantic_text
    FROM jobs
    ORDER BY id DESC
    LIMIT 3
    """
)

rows = cursor.fetchall()

for row in rows:

    print("\n================")

    print("TITLE:")
    print(row["title"])

    print("\nSEMANTIC TEXT:")
    print(row["semantic_text"])

connection.close()