from app.services.job_aggregator import fetch_all_jobs
from app.services.job_deduplicator import deduplicator_jobs

jobs = fetch_all_jobs()
jobs.extend(jobs[:5])

print(f"Total jobs before deduplication: {len(jobs)}")

deduplicated_jobs = deduplicator_jobs(jobs)
print(f"Total jobs after deduplication: {len(deduplicated_jobs)}")
