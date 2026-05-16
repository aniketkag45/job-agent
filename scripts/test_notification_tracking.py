from app.services.database import fetch_unnotified_jobs,mark_job_as_notified

jobs = fetch_unnotified_jobs()
print(f"\nUnnotified jobs from database: {len(jobs)}\n")
for job in jobs[:5]:  # Show only top 5 for testing
    print(job)
    mark_job_as_notified(job["id"])
    print("-" * 40)