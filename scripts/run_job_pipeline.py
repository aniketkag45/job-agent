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
    mark_job_as_notified,
    job_exists
)

from app.notifier.telegram_notifier import (
    send_telegram_message
)

from app.services.pipeline_metrics import (
    increment_metric,
    reset_metrics,
    get_metrics
)


def run_pipeline():

    start_time = time.time()

    reset_metrics()

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
            apply_link = job.get("apply_link")
            if job_exists(apply_link):
                increment_metric("duplicates_skipped")
                continue

            was_inserted = insert_job(job)

            if was_inserted:

                jobs_inserted_count += 1

                increment_metric(
                    "jobs_inserted"
                )

        print(
            "\nJobs saved to database."
        )

        unnotified_jobs = fetch_unnotified_jobs()

        print(
            f"\nFound {len(unnotified_jobs)} unnotified jobs."
        )

        top_jobs = sorted(
            unnotified_jobs,
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        for job in top_jobs[:5]:

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

            increment_metric(
                "alerts_sent"
            )

            mark_job_as_notified(
                job["id"]
            )

        execution_time = (
            time.time() - start_time
        )

        metrics = get_metrics()

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

            jobs_filtered,

            duplicates_skipped,

            scraper_failures,

            alerts_sent,

            status,

            execution_time_seconds

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            run_started_at,

            datetime.now().isoformat(),

            jobs_fetched_count,

            jobs_inserted_count,

            metrics["jobs_filtered"],

            metrics["duplicates_skipped"],

            metrics["scraper_failures"],

            alerts_sent_count,

            "SUCCESS",

            execution_time
        ))

        connection.commit()

        connection.close()

        print("\nPipeline Metrics Summary:\n")

        for key, value in metrics.items():

            print(f"{key}: {value}")

        print(
            f"\nPipeline execution completed in {execution_time:.2f} seconds."
        )

    except Exception as error:

        execution_time = (
            time.time() - start_time
        )

        metrics = get_metrics()

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

            jobs_filtered,

            duplicates_skipped,

            scraper_failures,

            alerts_sent,

            status,

            error_message,

            execution_time_seconds

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            run_started_at,

            datetime.now().isoformat(),

            jobs_fetched_count,

            jobs_inserted_count,

            metrics["jobs_filtered"],

            metrics["duplicates_skipped"],

            metrics["scraper_failures"],

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