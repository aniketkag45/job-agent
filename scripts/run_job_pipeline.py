import sqlite3
import traceback
import time
from datetime import datetime

from app.services.job_aggregator import fetch_all_jobs
from app.services.job_deduplicator import deduplicator_jobs
from app.services.job_filter import score_jobs
from app.utils.config_loader import load_user_preferences

from app.services.database import (
    insert_job,
    fetch_unnotified_jobs,
    mark_job_as_notified
)

from app.notifier.telegram_notifier import (
    send_telegram_message
)


def run_pipeline():

    start_time = time.time()

    run_started_at = datetime.now().isoformat()

    jobs_fetched_count = 0
    jobs_inserted_count = 0
    alerts_sent_count = 0

    try:

        print("\nStarting job pipeline...\n")

        jobs = fetch_all_jobs()

        jobs_fetched_count = len(jobs)

        print(
            f"Fetched {jobs_fetched_count} jobs from sources."
        )

        jobs = deduplicator_jobs(jobs)

        print(
            f"{len(jobs)} jobs after deduplication."
        )

        preferences = load_user_preferences()

        jobs = score_jobs(
            jobs,
            preferences
        )

        print(
            "Scored jobs based on user preferences."
        )

        for job in jobs:

            insert_job(job)

            jobs_inserted_count += 1

        print(
            "\nJobs saved to database."
        )

        unnotified_jobs = fetch_unnotified_jobs()

        print(
            f"\nFound {len(unnotified_jobs)} unnotified jobs."
        )

        for job in unnotified_jobs[:5]:

            message = f"""
🚀 New Job Found!

💼 {job['title']}

🏢 {job['company']}

📍 {job['location']}

⭐ Score: {job['score']}

🔗 {job['apply_link']}
"""

            send_telegram_message(message)

            alerts_sent_count += 1

            mark_job_as_notified(job["id"])

        execution_time = time.time() - start_time

        connection = sqlite3.connect(
            "database/jobs.db"
        )

        cursor = connection.cursor()

        cursor.execute("""

        INSERT INTO pipeline_runs (

            run_started_at,

            run_completed_at,

            jobs_fetched,

            jobs_inserted,

            alerts_sent,

            status,

            execution_time_seconds

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            run_started_at,

            datetime.now().isoformat(),

            jobs_fetched_count,

            jobs_inserted_count,

            alerts_sent_count,

            "SUCCESS",

            execution_time
        ))

        connection.commit()

        connection.close()

        print(
            f"\nPipeline execution completed in {execution_time:.2f} seconds."
        )

    except Exception as error:

        execution_time = time.time() - start_time

        connection = sqlite3.connect(
            "database/jobs.db"
        )

        cursor = connection.cursor()

        cursor.execute("""

        INSERT INTO pipeline_runs (

            run_started_at,

            run_completed_at,

            jobs_fetched,

            jobs_inserted,

            alerts_sent,

            status,

            error_message,

            execution_time_seconds

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            run_started_at,

            datetime.now().isoformat(),

            jobs_fetched_count,

            jobs_inserted_count,

            alerts_sent_count,

            "FAILED",

            str(error),

            execution_time

        ))

        connection.commit()

        connection.close()

        traceback.print_exc()


if __name__ == "__main__":

    run_pipeline()