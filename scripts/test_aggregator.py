from app.services.job_aggregator import fetch_all_jobs

jobs = fetch_all_jobs()

print(f"Aggregated {len(jobs)} jobs from all sources")

for job in jobs[:5]:
    print(job)
    print("-" * 40)
    