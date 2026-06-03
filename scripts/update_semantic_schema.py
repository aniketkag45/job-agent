from app.services.database import get_connection

connection = get_connection()

cursor = connection.cursor()

try:

    cursor.execute("""

    ALTER TABLE jobs

    ADD COLUMN semantic_text TEXT

    """)

    connection.commit()

    print(
        "Added semantic_text column."
    )

except Exception as error:

    print(
        f"Schema update skipped: "
        f"{error}"
    )

finally:

    connection.close()