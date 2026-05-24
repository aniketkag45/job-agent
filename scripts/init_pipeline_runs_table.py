import sqlite3


connection = sqlite3.connect(

    "database/jobs.db"
)

cursor = connection.cursor()


cursor.execute("""

CREATE TABLE IF NOT EXISTS pipeline_runs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_started_at TEXT,

    run_completed_at TEXT,

    jobs_fetched INTEGER DEFAULT 0,

    jobs_inserted INTEGER DEFAULT 0,

    alerts_sent INTEGER DEFAULT 0,

    status TEXT,

    error_message TEXT,

    execution_time_seconds REAL

)

""")


connection.commit()

connection.close()


print(
    "pipeline_runs table created successfully."
)