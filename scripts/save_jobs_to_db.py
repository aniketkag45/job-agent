from app.services.job_aggregator import fetch_all_jobs
from app.services.job_filter import score_jobs
from app.services.job_deduplicator import deduplicator_jobs
from app.services.database import insert_job
from app.utils.config_loader import load_user_preferences

jobs = fetch_all_jobs()
jobs = deduplicator_jobs(jobs)   
preferences =  load_user_preferences()
jobs = score_jobs(jobs, preferences)

for job in jobs:
    insert_job(job)

print("\nAll jobs have been processed and saved to the database.")