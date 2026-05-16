from app.services.job_aggregator import fetch_all_jobs

from app.services.job_filter import (
    score_jobs
)
from app.utils.config_loader import load_user_preferences

preferences = load_user_preferences()
jobs = fetch_all_jobs()
scored_jobs = score_jobs(jobs, preferences)

print(f"\nTop scored jobs:\n")


for job in scored_jobs[:10]:

    print(
        f"Score: {job['score']} | "
        f"{job['title']}"
    )

    print(job)

    print("-" * 50)