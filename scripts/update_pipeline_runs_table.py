import sqlite3


connection = sqlite3.connect(
    "database/jobs.db"
)

cursor = connection.cursor()


columns_to_add = [

    "jobs_filtered INTEGER DEFAULT 0",

    "duplicates_skipped INTEGER DEFAULT 0",

    "scraper_failures INTEGER DEFAULT 0"
]


for column in columns_to_add:

    try:

        cursor.execute(
            f"""
            ALTER TABLE pipeline_runs
            ADD COLUMN {column}
            """
        )

        print(
            f"Added column: {column}"
        )

    except sqlite3.OperationalError as error:

        print(
            f"Skipping existing column: {column}"
        )


connection.commit()

connection.close()


print(
    "\nPipeline runs table updated successfully."
)