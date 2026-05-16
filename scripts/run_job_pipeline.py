from app.services.job_aggregator import fetch_all_jobs
from app.services.job_deduplicator import deduplicator_jobs
from app.services.job_filter import score_jobs
from app.utils.config_loader import load_user_preferences
from app.services.database import insert_job,fetch_unnotified_jobs,mark_job_as_notified
from app.notifier.telegram_notifier import send_telegram_message

def run_pipeline():
    print("\nStarting job pipeline...\n")
    jobs = fetch_all_jobs()
    print(f"Fetched {len(jobs)} jobs from sources.")
    jobs = deduplicator_jobs(jobs)
    print(f"{len(jobs)} jobs after deduplication.")
    preferences =  load_user_preferences()
    jobs = score_jobs(jobs, preferences)
    print(f"Scored jobs based on user preferences.")
    for job in jobs:
        insert_job(job)
    print("\njobs saved to database.")
    unnotified_jobs = fetch_unnotified_jobs()
    print(f"\nFound {len(unnotified_jobs)} unnotified jobs.")
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

        mark_job_as_notified(job["id"])

    print(
        "\nPipeline execution completed."
    )


if __name__ == "__main__":

    run_pipeline()